from django_redis import get_redis_connection

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from goods.models import GoodsSKU
from utils.mixin import LoginRequiredMixin


def check_cart_input(request, with_count=True):
    """
    校验修改购物车时，传入的数据是否合法

    :param request: request 请求
    :param with_count: True 表示请求中含有商品数目， false 表示不含有
    :return: goods_sku: 查询到的商品实例
    :return: count:  购物车中商品的数量
    """
    # ajax　发起的请求都在后台，不能使用　LoginRequiredMixin 进行装饰
    user = request.user
    if not user.is_authenticated:
        # 用户未登录
        raise ValueError(JsonResponse({'res': 1, 'error_msg': '用户未登录'}))
    # 获取数据
    sku_id = request.POST.get("sku_id")
    # 为了后续校验数据完整性，如果 with_count 为 False， 则将 count 置为 True
    count = request.POST.get("count") if with_count else True
    # 校验数据完整性
    if not all([sku_id, count]):
        raise ValueError(JsonResponse({'res': 2, 'error_msg': '数据不完整'}))
    # 校验商品数据
    if with_count:
        try:
            count = int(count)
            if count <= 0:
                raise ValueError
        except ValueError:
            raise ValueError(JsonResponse({'res': 3, 'error_msg': '商品数目出错!'}))
    # 检查商品是否存在
    try:
        goods_sku = GoodsSKU.objects.get(id=sku_id)
    except GoodsSKU.DoesNotExist:
        raise ValueError(JsonResponse({'res': 4, 'error_msg': '商品不存在'}))

    return goods_sku, count


# /cart/add_cart
class AddCartView(View):
    """
    添加商品到购物车
    """
    def post(self, request):
        """
        处理 ajax 发送的异步请求
        """
        # 校验输入是否要求
        try:
            goods_sku, count = check_cart_input(request)
        except ValueError as exc:
            return exc.args[0]

        # 进行业务处理
        conn = get_redis_connection('default')
        cart_id = "cart_%d" % request.user.id
        # 获取购物车中现在的当前商品的数目
        current_count = conn.hget(cart_id, goods_sku.id)
        if current_count is not None:
            count += int(current_count)

        if count > goods_sku.stock:
            return JsonResponse({'res': 5, 'error_msg': '库存不足'})
        # 更新商品数量
        conn.hset(cart_id, goods_sku.id, count)
        # 获取当前购物车中的商品种类数目
        goods_num = conn.hlen(cart_id)

        # 返回应答
        return JsonResponse({'res': 0, 'goods_num': goods_num})


# /cart/
class ShowCartView(LoginRequiredMixin, View):
    """
    显示购物车页面
    """
    def get(self, request):
        """
        显示购物车页面
        """
        # 从　redis　中获取购物车中商品的相关信息
        conn = get_redis_connection("default")
        cart_id = "cart_%d" % request.user.id
        cart_dict = conn.hgetall(cart_id)
        # 组织相关数据
        skus = list()
        goods_amount = 0
        goods_amount_price = 0
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            sku.count = int(count)
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
    """
    更新购物车记录
    """
    def post(self, request):
        """
        接收 ajax 的 post 请求, 更新购物车数据
        """
        try:
            goods_sku, count = check_cart_input(request)
        except ValueError as exc:
            return exc.args[0]

        if count > goods_sku.stock:
            return JsonResponse({'res': 5, 'error_msg': '库存不足'})

        conn = get_redis_connection("default")
        cart_id = "cart_%d" % request.user.id
        conn.hset(cart_id, goods_sku.id, count)
        # 计算出商品的总件数
        goods_num = 0
        for item in conn.hvals(cart_id):
            goods_num += int(item)
        return JsonResponse({'res': 0, 'goods_num': goods_num})


# /cart/delete_cart
class DeleteCartView(View):
    """
    删除购物车中的商品
    """
    def post(self, request):
        """
        Ajax post 请求
        """
        try:
            goods_sku, _ = check_cart_input(request, with_count=False)
        except ValueError as exc:
            return exc.args[0]
        # 进行删除操作
        conn = get_redis_connection("default")
        cart_id = 'cart_%d' % request.user.id
        conn.hdel(cart_id, goods_sku.id)
        # 计算出商品的总件数
        goods_num = 0
        for item in conn.hvals(cart_id):
            goods_num += int(item)
        return JsonResponse({'res': 0, 'goods_num': goods_num})

