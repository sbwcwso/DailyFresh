import time

from django_redis import get_redis_connection
from haystack.views import SearchView

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.urls import reverse

from goods.models import (
    GoodsType, IndexTypeGoodsBanner, IndexGoodsBanner,
    IndexPromotionBanner, GoodsSKU,
)
from order.models import OrderGoods
from utils.mixin import ListViewMixin, SearchViewMixin


# Create your views here.


# /
class IndexView(View):
    """
    首页的类视图
    """

    def get(self, request):
        """
        返回首页的网页
        """
        get_info = request.GET.get("get_info")
        if get_info == '1':
            return self.get_info(request)
        content_text = cache.get('index_page_data')
        if content_text is None:  # 缓存中没有数据,则从数据库中进行楂询
            # 从 mysql 数据库中查询品相关信息
            content_text = self.get_content_text()

            cache.set('index_page_data', content_text, 3600)

        # 用户登录后,则获取购物车的数目, 从 redis 中查购物车的数目
        cart_num = 0
        user = request.user
        if user.is_authenticated:
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)
        content_text.update(cart_num=cart_num)

        return render(request, 'index.html', content_text)

    @staticmethod
    def get_info(request):
        """
        静态页面的 post 请求, 查看用户是否登录, 如果登录,则获取购物车数目
        """
        user = request.user
        if user.is_authenticated:
            username = user.username
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)
            return JsonResponse({"res": 1, 'username': username, 'cart_num': cart_num})
        return JsonResponse({"res": 0})

    @staticmethod
    def get_content_text():
        """
        从数据库中查询首询首页所需要的相关信息

        :return:

        context: dict
        """
        # 获取所有的商品类型
        types = GoodsType.objects.all()
        banners = IndexGoodsBanner.objects.all().order_by("index")
        # 根据获取的商品类型查询首页要展示的商品
        for goods_type in types:
            # 获取文字信息
            goods_type.titles = IndexTypeGoodsBanner.objects.filter(type=goods_type,
                                                                    display_type=0).order_by("index")
            # 获取图片信息
            goods_type.images = IndexTypeGoodsBanner.objects.filter(type=goods_type,
                                                                    display_type=1).order_by("index")
        promotion_banner = IndexPromotionBanner.objects.all().order_by("index")

        content_text = {
            "types": types,
            "banners": banners,
            "promotion_banners": promotion_banner,
        }
        return content_text


# /goods/商品id
class DetailView(View):
    """
    商品详情页
    """

    def get(self, request, goods_id):
        """
        显示详情页
        """
        # 从数据库中查取相关数据, 判断商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在,则返回首页
            return redirect(render("goods:index"))
        # 获取所有的分类信息
        types = GoodsType.objects.all()
        # 获取商品的评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment="")
        new_skus = GoodsSKU.objects.filter(type=sku.type).exclude(id=sku.id).order_by("-create_time")[:2]
        # 查询 spu 相同的商品,以集中展示
        same_spus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=sku.id)

        # 从 redis 中查购物车的数目, 以及保存相应的用户浏览记录
        cart_num = 0
        user = request.user
        if user.is_authenticated:
            # 用户登录后,则获取购物车的数目
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)
            # 更新用户的浏览记录
            history_key = "history_%d" % user.id
            conn.zadd(history_key, time.time(), sku.id)
            # 只保留 10 条浏览记录，后添加的记录排在后面，相当于保留第 -10 至 -1 条数据
            conn.zremrangebyrank(history_key, 0, -11)

        content_text = {
            'sku': sku,
            'types': types,
            'sku_orders': sku_orders,
            'same_spus': same_spus,
            'new_skus': new_skus,
            'cart_num': cart_num,
        }

        return render(request, "detail.html", content_text)


# /list/种类id/页码?sort=排序方式
class GoodsListView(ListViewMixin, ListView):
    """列表页"""
    paginate_by = 3  # 每页显示的页数
    template_name = 'list.html'

    def get(self, request, type_id, page):
        """返回列表页面"""
        # 获取商品种类信息,如果不存在,则返回首页
        if type_id != '0':
            try:
                goods_type = GoodsType.objects.get(id=type_id)
            except GoodsType.DoesNotExist:
                return redirect(reverse('goods:index'))
        else:
            goods_type = GoodsType()
            goods_type.id = 0

        # 获取所有商品分类信息
        types = GoodsType.objects.all()

        # 获取同一种类下所有的商品信息, 按照相应的方法进行排序
        sort = request.GET.get('sort')
        # sort: default, price, hot
        if type_id != '0':
            skus = GoodsSKU.objects.filter(type=goods_type)
        else:
            skus = GoodsSKU.objects.all()
        if sort == "price":
            skus = skus.order_by("price")
        elif sort == "hot":
            skus = skus.order_by("-sales")
        else:
            skus = skus.order_by("-id")
            sort = "default"

        # 获取新品信息
        new_skus = skus.order_by("-create_time")[:2]

        # 获取购物车相关信息
        user = request.user
        cart_num = 0
        if user.is_authenticated:
            # 用户登录后,则获取购物车的数目
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)

        self.object_list = skus

        context = {
            "type": goods_type,
            "types": types,
            "new_skus": new_skus,
            "cart_num": cart_num,
            "sort": sort,
        }
        context = self.get_context_data(**context)
        return self.render_to_response(context)


class NewSearchView(SearchViewMixin, SearchView):
    """
    自定义的 haystack 商品搜索类
    """