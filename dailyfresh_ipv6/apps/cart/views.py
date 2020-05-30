from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin

# Create your views here.


# /cart/add_cart
class AddCartView(View):
    """添加购物车的操作"""
    def post(self, request):
        """处理 ajax 发送的异步请求"""
        user = request.user
        if not user.is_authenticated:
            """用户未登录"""
            return JsonResponse({'res': 0, 'error_msg': '用户未登录'})
        # 获取数据
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # 校验数据
        try:
            goods_sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 1, 'error_msg': '添加的商品不存在'})

        try:
            count = int(count)
            if count <= 0:
                raise Exception
        except Exception:
            return JsonResponse({'res': 2, 'error_msg': '非法请求'})

        # 进行业务处理
        conn = get_redis_connection('default')
        cart_id = "cart_%d" % user.id
        # 获取购物车中现在的当前商品的数目
        current_count = conn.hget(cart_id, goods_sku.id)
        if current_count is not None:
            count += int(current_count)

        if count > goods_sku.stock:
            return JsonResponse({'res': 3, 'error_msg': '库存不足'})
        # 更新商品数量
        conn.hset(cart_id, goods_sku.id, count)
        # 获取当前购物车中的商品种类数目
        goods_num = conn.hlen(cart_id)

        # 返回应答
        return JsonResponse({'res': 4, 'goods_num': goods_num})


# /cart/show_cart
class ShowCartView(LoginRequiredMixin, View):
    """显示购物车页面"""
    def get(self, request):
        # 查询相关的数据
        conn = get_redis_connection("default")
        cart_id = "cart_%d" % request.user.id
        skus_id = conn.hkeys(cart_id)

        skus = list()
        goods_amount = 0
        goods_amount_price = 0
        for sku_id in skus_id:
            sku = GoodsSKU.objects.get(id=sku_id)
            sku.count = int(conn.hget(cart_id, sku_id))
            sku.amount = sku.price * sku.count
            goods_amount += sku.count
            goods_amount_price += sku.amount
            skus.append(sku)
        # 组织模板上下文,并返回
        return render(request, "cart.html", {
            "skus": skus,
            "goods_amount": goods_amount,
            "goods_amount_price": goods_amount_price,
        })


# /cart/update_cart
class UpdateCartView(View):
    """更新购物车记录"""
    def post(self, request):
        """接收 ajax 的 post 请求, 更新购物车数据"""
        user = request.user
        if not user.is_authenticated:
            """用户未登录"""
            return JsonResponse({'res': 0, 'error_msg': '用户未登录'})
        # 获取数据
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # 校验数据
        try:
            goods_sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 1, 'error_msg': '添加的商品不存在'})

        try:
            count = int(count)
            if count <= 0:
                raise Exception
        except Exception:
            return JsonResponse({'res': 2, 'error_msg': '非法请求'})

        if count > goods_sku.stock:
            return JsonResponse({'res': 3, 'error_msg': '库存不足'})

        conn = get_redis_connection("default")
        cart_id = "cart_%d" % user.id
        conn.hset(cart_id, goods_sku.id, count)
        # 计算出商品的总件数
        vals = conn.hvals(cart_id)
        amounts = 0
        for item in vals:
            amounts += int(item)
        return JsonResponse({'res': 4, 'amounts': amounts})


# /cart/delete_cart
class DeleteCartView(View):
    """删除购物车中的商品"""
    def post(self, request):
        """Ajax post 请求"""
        user = request.user
        if not user.is_authenticated:
            """用户未登录"""
            return JsonResponse({'res': 0, 'error_msg': '用户未登录'})
        # 获取数据
        sku_id = request.POST.get("sku_id")

        # 校验数据
        try:
            goods_sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 1, 'error_msg': '要删除的商品不存在'})

        # 进行删除操作
        conn = get_redis_connection("default")
        cart_id = 'cart_%d' % user.id
        conn.hdel(cart_id, goods_sku.id)

        # 返回应答和总商品的件数
        all_vals = conn.hvals(cart_id)
        amount = 0
        for val in all_vals:
            amount += int(val)
        return JsonResponse({'res': 2, 'amount': amount})


