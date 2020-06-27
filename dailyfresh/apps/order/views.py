from datetime import datetime
import time

from django_redis import get_redis_connection

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from user.models import Address
from utils.mixin import LoginRequiredMixin


# /order/place
class OrderPlaceView(LoginRequiredMixin, View):
    """
    提交订单页面显示
    """
    def post(self, request):
        """
        提交订单页面的显示
        """
        # 获取相关的参数
        sku_ids = request.POST.getlist("sku_id")
        # 校验数据完整性
        if not sku_ids:
            return redirect(reverse("cart:show_cart"))

        # 从数据库中查询相关信息
        # 查询商品信息
        conn = get_redis_connection("default")
        cart_key = "cart_%d" % request.user.id
        skus = []
        total_count, total_amount = 0, 0
        for sku_id in sku_ids:
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                # todo 添加过几秒后自动跳转的功能
                return HttpResponse("<h2>请求的商品不存在.</h2><br><a href='/'>返回首页<a>" % email)
            sku.count = int(conn.hget(cart_key, sku.id))
            sku.amount = sku.price * sku.count
            skus.append(sku)

            total_amount += sku.amount
            total_count += sku.count
        # todo 运费, 可由专门的子系统进行处理
        trans_price = 10
        # 获取用户地址
        addresses = Address.objects.filter(user=request.user)
        # 实付歀
        total_price = total_amount + trans_price
        # 拼接商品的 id
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
class OrderCommitView(View):
    """
    订单确认--乐观锁
    """
    @transaction.atomic
    def post(self, request):
        """
        ajax post 请求，后台生成订单
        """
        # 验证用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 1, 'error_msg': '用户未登录'})
        # 接收相关的参数
        pay_method = request.POST.get("pay_method")
        addr_id = request.POST.get("addr_id")
        sku_ids = request.POST.get("sku_ids")
        # 检验数据完整性
        if not all([pay_method, addr_id, sku_ids]):
            return JsonResponse({'res': 2, 'error_msg': '参数不完整, 请检查是否缺少默认的收货地址'})
        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHOD.keys():
            # todo： 添加其它支付方式
            if pay_method != '3':
                return JsonResponse({'res': 3, 'error_msg': '非法的支付请求, 目前只支持模拟支付宝登录'})
        # 校验收货地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 4, 'error_msg': '地址不存在'})

        # 设置事务保存点
        sid = transaction.savepoint()
        # 尝试添加订单信息
        try:
            # 运费
            trans_price = 10
            # 总商品数
            total_count = 0
            # 商品总价格
            total_price = 0
            order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)  # 201808081020(年月日时分秒)+user_id
            order_info = OrderInfo.objects.create(order_id=order_id, user=user, addr=addr,
                                                  pay_method=pay_method, total_count=total_count,
                                                  total_price=total_price, transit_price=trans_price,
                                                  )
            # 添加订单商品信息表
            conn = get_redis_connection('default')
            cart_key = "cart_%d" % user.id
            sku_ids = sku_ids.split(",")
            # 尝试次数
            try_times = 3
            for sku_id in sku_ids:
                for i in range(try_times):
                    try:
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'res': 5, 'error_msg': '商品不存在'})
                    count = int(conn.hget(cart_key, sku.id))  # 从 redis 中获取商品数量
                    # 校验商品库存, 并进行更新
                    if sku.stock < count:
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'res': 6, 'error_msg': '商品库存不足'})

                    # 乐观锁, 首先检查当前的数据和之前查出的数据是否相同, 如果相同,才更新数据, 仍然会阻塞, 但查询时不会堵塞
                    res = GoodsSKU.objects.filter(id=sku.id, stock=sku.stock).update(stock=sku.stock - count,
                                                                                     sales=sku.sales + count)
                    if res == 0:
                        if i == try_times - 1:
                            transaction.savepoint_rollback(sid)
                            return JsonResponse({'res': 7, 'error_msg': '下单失败'})
                    else:
                        # 更新成功，写入数据库，提交事务，跳出乐观锁循环
                        order_good = OrderGoods.objects.create(order=order_info,
                                                               sku=sku, count=count, price=count * sku.price)
                        total_count += count
                        total_price += order_good.price
                        break
            # 更新订单信息中的商品总价数和总价格
            order_info.total_price = total_price
            order_info.total_count = total_count
            order_info.save()
        except Exception as err:
            transaction.savepoint_rollback(sid)
            return JsonResponse({'res': 8, 'error_msg': '下单失败{}'.format(err.args)})
        else:
            # 订单中的所有商品均更新成功，提交事务
            transaction.savepoint_commit(sid)
            # 删除购物车中的相关商品
            conn.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 0})


# /oder/pay
class OrderPayView(View):
    """
    调用 alipay 接口进行支付
    """
    def post(self, request):
        """
        ajax post 进行支付
        """
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 1, 'error_msg': '用户未登录'})
        # 接收参数
        order_id = request.POST.get('order_id')
        # 校验参数
        if not order_id:
            return JsonResponse({'res': 2, 'error_msg': '参数不完整'})
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=1, pay_method=3)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 3, 'error_msg': '订单错误'})
        # 业务处理: 使用 Python sdk 调用支付宝接口支付
        # 调用 api 接口
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        total_amount = order.total_price + order.transit_price
        subject = "天天生鲜_%s" % order.order_id + " 沙箱测试，请选择登录帐户支付，帐号及密码见订单详情"
        body = "测试用支付帐号：dsgsme3919@sandbox.com, 登录密码：111111, 支付密码：111111"
        order_string = settings.ALIPAY.api_alipay_trade_page_pay(
            out_trade_no=order.order_id,
            total_amount=str(total_amount),
            subject=subject,
            body=body,
            return_url="http://dailyfresh.alijunjiea.com/order/check",
            notify_url="http://dailyfresh.alijunjiea.com/order/notify",
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        # todo: 返回应答
        return JsonResponse({'res': 0, 'pay_url': pay_url})


# /order/check
class OrderCheckView(View):
    """
    Alipay return url 返回的地址
    """
    def get(self, request):
        """Alipay 访问 return url"""
        data = request.GET.dict()
        signature = data.pop("sign")
        # 验证数据
        success = settings.ALIPAY.verify(data, signature) if all([data, signature]) else False
        if success:
            order_id = data.get("out_trade_no", None)
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except OrderInfo.DoesNotExist:
                return "<h2>订单错误</h2>"
            response = settings.ALIPAY.api_alipay_trade_query(out_trade_no=order.order_id)
            code = response['code']
            if code == "10000" and response['trade_status'] == 'TRADE_SUCCESS':
                # 支付成功, 返回结果
                return HttpResponse('<h2>订单支付完成</h2><br><a href={}>前往订单页面</a>'
                                    .format(reverse('user:order', kwargs={'page': 1})))
            else:
                return HttpResponse('<h2>订单异常!</h2><br><a href={}>前往订单页面</a>'
                                    .format(reverse('user:order', kwargs={'page': 1})))
        return HttpResponse('<h2>非法请求</h2><br><a href={}>前往订单页面</a>'
                            .format(reverse('user:order', kwargs={'page': 1})))


# /order/notify
class OrderNotifyView(View):
    """
    Alipay 通过 notifyurl 来更新订单的状态
    """
    # @csrf_exempt
    def post(self, request):
        """
        Alipay 通过　post 请求访问　notifyurl
        """
        data = request.POST.dict()
        signature = data.pop("sign")

        # 验证数据
        success = settings.ALIPAY.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            order_id = data.get("out_trade_no", None)
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except OrderInfo.DoesNotExist:
                return "<h2>订单错误</h2>"
            # 支付成功,更新订单状态,并返回结果
            order.trade_no = data['trade_no']
            order.order_status = 4  # 直接设置为待评价
            order.save()


# /order/comment/oder_id
class OrderCommentView(LoginRequiredMixin, View):
    """
    订单评论
    """
    def get(self, request, order_id):
        """
        get 请求, 显示评论页面
        """
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
        """
        post 请求, 向数据库中添加评论信息
        """
        # 获取相关参数
        order_id = request.POST.get('order_id')
        # 校验参数
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=4)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))
        # 获取并添加评论信息
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



