from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from user.models import Address
from order.models import OrderInfo, OrderGoods
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.db import transaction
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# Create your views here.


# /order/place
class OrderPlaceView(LoginRequiredMixin, View):
    """提交订单页面"""
    def post(self, request):
        # 获取相关的参数
        sku_ids = request.POST.getlist("sku_id")

        # 校验数据
        if not sku_ids:
            return redirect(reverse("cart:show_cart"))

        # 从数据库中查询相关信息
        # 查询商品信息
        skus = list()
        conn = get_redis_connection("default")
        total_count = 0
        total_amount = 0
        for sku_id in sku_ids:
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                return HttpResponse("<h2>请求的商品不存在.</h2><br><a href='/'>返回首页<a>" % email)
            cart_id = "cart_%d" % request.user.id
            sku.count = int(conn.hget(cart_id, sku.id))
            sku.amount = sku.price * sku.count
            skus.append(sku)

            total_amount += sku.amount
            total_count += sku.count
        # 运费,一般由专门的子系统进行处理
        trans_price = 10
        # 获取用户地址
        addresses = Address.objects.filter(user=request.user)
        total_price = total_amount + trans_price

        # 拼拼商品的 id
        sku_ids = ",".join(sku_ids)

        # 组织模板上下文
        content_text = {
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'trans_price': trans_price,
            'total_price': total_price,
            'addresses': addresses,
            'sku_ids': sku_ids,
        }

        return render(request, "place_order.html", content_text)


# /order/commit
class OrderCommitView1(View):
    """订单确认--悲观锁--运行时会堵塞"""
    @transaction.atomic
    def post(self, request):
        """ajax post 请求"""
        # 验证用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 1, 'error_msg': '用户未登录'})
        # 获取相关的参数
        pay_method = request.POST.get("pay_method")
        addr_id = request.POST.get("addr_id")
        sku_ids = request.POST.get("sku_ids")

        # 检验数据
        if not all([pay_method, addr_id, sku_ids]):
            return JsonResponse({'res': 2, 'error_msg': '数据不完整'})

        if pay_method not in OrderInfo.PAY_METHOD.keys():
            return JsonResponse({'res': 3, 'error_msg': '非法的支付请求'})

        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 4, 'error_msg': '地址不存在'})

        sid = transaction.savepoint()
        # todo: 添加订单信息
        # 组织数据
        trans_price = 10  # 运费
        total_count = 0  # 总商品数
        total_price = 0  # 商品总价格
        order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)  # 201808081020(年月日时分秒)+user_id
        order_info = OrderInfo.objects.create(order_id=order_id, user=user, addr=addr,
                                              pay_method=pay_method, total_count=total_count,
                                              total_price=total_price, transit_price=trans_price,
                                              )
        # todo: 添加订单商品信息表
        conn = get_redis_connection('default')
        cart_id = "cart_%d" % user.id
        sku_ids = sku_ids.split(",")

        for sku_id in sku_ids:
            try:
                sku = GoodsSKU.objects.select_for_update().get(id=sku_id)  # 悲观锁,事务结束后锁释放
            except GoodsSKU.DoesNotExist:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 5, 'error_msg': '商品不存在'})
            count = int(conn.hget(cart_id, sku.id))  # 从 redis 中获取商品数量
            import time
            time.sleep(10)
            print("%d : %d" % (user.id, sku.stock))
            # 校验商品库存, 并进行更新
            if sku.stock < count:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 6, 'error_msg': '商品库存不足'})

            sku.stock -= count
            sku.sales += count
            sku.save()
            # 写入数据库
            order_good = OrderGoods.objects.create(order=order_info, sku=sku, count=count, price=count * sku.price)
            total_count += count
            total_price += order_good.price
        # 更新订单信息中的商品总价数和总价格
        order_info.total_price = total_price
        order_info.total_count = total_count
        order_info.save()
        # 结束事务
        transaction.savepoint_commit(sid)

        # todo: 删除购物车中的相关商品
        conn.hdel(cart_id, *sku_ids)

        return JsonResponse({'res': 0})


# /order/commit
class OrderCommitView(View):
    """订单确认--乐观锁"""
    @transaction.atomic
    def post(self, request):
        """ajax post 请求"""
        # 验证用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 1, 'error_msg': '用户未登录'})
        # 获取相关的参数
        pay_method = request.POST.get("pay_method")
        addr_id = request.POST.get("addr_id")
        sku_ids = request.POST.get("sku_ids")

        # 检验数据
        if not all([pay_method, addr_id, sku_ids]):
            return JsonResponse({'res': 2, 'error_msg': '数据不完整'})

        if pay_method not in OrderInfo.PAY_METHOD.keys():
            return JsonResponse({'res': 3, 'error_msg': '非法的支付请求'})

        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 4, 'error_msg': '地址不存在'})

        sid = transaction.savepoint()
        try:
            # todo: 添加订单信息
            # 组织数据
            trans_price = 10  # 运费
            total_count = 0  # 总商品数
            total_price = 0  # 商品总价格
            order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)  # 201808081020(年月日时分秒)+user_id
            order_info = OrderInfo.objects.create(order_id=order_id, user=user, addr=addr,
                                                  pay_method=pay_method, total_count=total_count,
                                                  total_price=total_price, transit_price=trans_price,
                                                  )
            # todo: 添加订单商品信息表
            conn = get_redis_connection('default')
            cart_id = "cart_%d" % user.id
            sku_ids = sku_ids.split(",")
            try_times = 3
            for sku_id in sku_ids:
                for i in range(try_times):
                    try:
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'res': 5, 'error_msg': '商品不存在'})
                    count = int(conn.hget(cart_id, sku.id))  # 从 redis 中获取商品数量
                    # 校验商品库存, 并进行更新
                    if sku.stock < count:
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'res': 6, 'error_msg': '商品库存不足'})

                    # 乐观锁, 首先检查当前的数据和之前查出的数据是否相同, 如果相同,才更新数据, 仍然会阻塞, 但查询时不会堵塞
                    res = GoodsSKU.objects.filter(id=sku.id, stock=sku.stock).update(stock=sku.stock - count,
                                                                                     sales=sku.sales + count)
                    print("%d : %d" % (user.id, sku.stock))
                    if res == 0:
                        if i == try_times - 1:
                            # 更改的行数为0, 则已尝试了给定的次数,说明更新失败
                            transaction.savepoint_rollback(sid)
                            return JsonResponse({'res': 7, 'error_msg': '下单失败--乐观锁生效'})
                        continue
                    # 写入数据库
                    order_good = OrderGoods.objects.create(order=order_info, sku=sku, count=count, price=count * sku.price)
                    total_count += count
                    total_price += order_good.price
                    break  # 跳出循环
            # 更新订单信息中的商品总价数和总价格
            order_info.total_price = total_price
            order_info.total_count = total_count
            order_info.save()
            # 提交事务
            transaction.savepoint_commit(sid)
        except Exception as err:
            transaction.savepoint_rollback(sid)
            return JsonResponse({'res': 8, 'error_msg': '下单失败' + repr(err)})

        # todo: 删除购物车中的相关商品
        conn.hdel(cart_id, *sku_ids)

        return JsonResponse({'res': 0})


# /oder/pay
class OrderPayView(View):
    """调用 alipay 接口进行支付"""
    def post(self, request):
        """ajax post 进行支付"""
        # todo: 判断用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 1, 'errmsg': '用户未登录'})
        # todo: 接收参数
        order_id = request.POST.get('order_id')
        # todo: 校验参数
        if not order_id:
            return JsonResponse({'res': 2, 'errmsg': '参数不完整'})
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=1, pay_method=3)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '订单错误'})
        # todo: 业务处理: 使用 Python sdk 调用支付宝接口支付
        # 调用 api 接口
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        total_amount = order.total_price + order.transit_price
        subject = "天天生鲜_%s" % order.order_id
        order_string = settings.ALIPAY.api_alipay_trade_page_pay(
            out_trade_no=order.order_id,
            total_amount=str(total_amount),
            subject=subject,
            return_url="http://dailyfresh.ignorelist.com/order/check",
            notify_url="http://45.77.124.42/order/notify",  # 可选, 不填则使用默认notify url
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        # todo: 返回应答
        return JsonResponse({'res': 0, 'pay_url': pay_url})


# /order/check
class OrderCheckView(View):
    """订单支付状态查询"""
    def get(self, request):
        """Alipay 访问 return url"""
        data = request.GET.dict()
        signature = data.pop("sign")

        # 验证数据
        success = settings.ALIPAY.verify(data, signature)
        if success:
            order_id = data.get("out_trade_no", None)
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except OrderInfo.DoesNotExist:
                return "<h2>订单错误<\h2>"
            response = settings.ALIPAY.api_alipay_trade_query(out_trade_no=order.order_id)
            code = response['code']
            if code == "10000" and response['trade_status'] == 'TRADE_SUCCESS':
                # 支付成功,更新订单状态,并返回结果
                order.trade_no = data['trade_no']
                order.order_status = 4  # 直接设置为待评价
                order.save()
                return HttpResponse("<h2>订单支付成功!!</h2><br><a href='/user/order/1'>前往订单页面<a>")
            else:
                return HttpResponse("<h2>订单异常!</h2><br><a href='/user/order/1'>前往订单页面<a>")
        return HttpResponse("<h2>非法请求!</h2><br><a href='/user/order/1'>前往订单页面<a>")

    def post(self, request):
        """ajax post 获取支付状态"""
        # todo: 判断用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 1, 'errmsg': '用户未登录'})
        # todo: 接收参数
        order_id = request.POST.get('order_id')
        # todo: 校验参数
        if not order_id:
            return JsonResponse({'res': 2, 'errmsg': '参数不完整'})
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=1, pay_method=3)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '订单错误'})
        # todo: 业务处理: 使用 Python sdk 调用支付宝接口支付
        # 调用 api 接口
        while True:
            count += 1
            settings.ALIPAY.verify()
            response = settings.ALIPAY.api_alipay_trade_query(out_trade_no=order.order_id)
            code = response['code']
            if code == "10000" and response['trade_status'] == 'TRADE_SUCCESS':
                # 支付成功,更新订单状态,并返回结果
                order.trade_no = response['trade_no']
                order.order_status = 4  # 直接设置为待评价
                order.save()
                return JsonResponse({'res': 0})
            elif code == "40004" or (code == "10000" and response['trade_status'] == 'WAIT_BUYER_PAY'):
                # 业务处理失败或等待用户付款, 等待一段时间后继续尝试
                time.sleep(10)
                continue
            else:
                return JsonResponse({'res': 4, 'errmsg': '支付失败'})


# /order/notify
class OrderNotifyView(View):
    """通过 notifyurl 判断订单是否支付成功"""
    # @csrf_exempt
    def post(self, request):
        data = request.POST.dict()
        signature = data.pop("sign")

        # 验证数据
        success = settings.ALIPAY.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            order_id = data.get("out_trade_no", None)
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except OrderInfo.DoesNotExist:
                return "<h2>订单错误<\h2>"
            # 支付成功,更新订单状态,并返回结果
            order.trade_no = data['trade_no']
            order.order_status = 4  # 直接设置为待评价
            order.save()
            return HttpResponse("<h2>订单支付成功!!</h2><br><a href='/user/order/1'>前往订单页面<a>")

        return HttpResponse("<h2>非法请求!</h2><br><a href='/user/order/1'>前往订单页面<a>")


# /order/comment/oder_id
class OrderCommentView(LoginRequiredMixin, View):
    """定单评论"""
    def get(self, request, order_id):
        """get 请求, 显示评论页面"""
        # todo: 校验参数
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=4)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order", kwargs={'page': 1}))
        # 获取订单状态的标题
        order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
        # 获取订单中所有的商品
        order.order_skus = OrderGoods.objects.filter(order_id=order_id)
        content_text = {'order': order}
        return render(request, 'order_comment.html', content_text)

    @transaction.atomic
    def post(self, request, order_id):
        """post 请求, 向数据库中添加评论信息"""
        # todo: 获取相关参数
        order_id = request.POST.get('order_id')
        # todo: 校验参数
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=4)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))
        # todo: 获取并添加评论信息
        order_goods = OrderGoods.objects.filter(order_id=order_id)
        total_count = len(order_goods)  # 商品的种类数
        sid = transaction.savepoint()
        for count in range(1, total_count + 1):
            order_good_id = request.POST.get("order_goods_%d" % count)
            try:
                order_good = OrderGoods.objects.get(id=order_good_id)
            except OrderGoods.DoesNotExist:
                transaction.savepoint_rollback(sid)
                return redirect(reverse("user:order", kwargs={'page': 1}))
            comment = request.POST.get("content_%d" % count)
            order_good.comment = comment
            order_good.save()
        order.order_status = 5
        order.save()
        transaction.savepoint_commit(sid)
        return redirect(reverse("user:order", kwargs={'page': 1}))



