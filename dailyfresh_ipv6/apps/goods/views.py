from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from goods.models import GoodsType, IndexTypeGoodsBanner, IndexGoodsBanner, IndexPromotionBanner, GoodsSKU
from order.models import OrderGoods
from django_redis import get_redis_connection
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# Create your views here.


# /
class IndexView(View):
    """首页的类视图"""
    def get(self, request):
        """返回首页的网页"""
        get_info = request.GET.get("get_info")
        if get_info == '1':
            return self.get_info(request)
        content_text = cache.get('index_page_data')
        if not content_text:  # 缓存中没有数据,则从数据库中进行楂询
            # 从 mysql 数据库中查询商品相关信息
            goods_types = GoodsType.objects.all()
            banners = IndexGoodsBanner.objects.all().order_by("index")
            for goods_type in goods_types:
                goods_type.titles = IndexTypeGoodsBanner.objects.filter(type=goods_type, display_type=0).order_by("index")
                goods_type.images = IndexTypeGoodsBanner.objects.filter(type=goods_type, display_type=1).order_by("index")
            promotion_banner = IndexPromotionBanner.objects.all().order_by("index")

            content_text = {
                "types": goods_types,
                "banners": banners,
                "promotion_banners": promotion_banner,
            }

            cache.set('index_page_data', content_text, 3600)

        # 从 redis 中查购物车的数目
        cart_num = 0
        user = request.user
        if user.is_authenticated:
            # 用户登录后,则获取购物车的数目
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)
        content_text.update(cart_num=cart_num)

        return render(request, 'index.html', content_text)

    @staticmethod
    def get_info(request):
        """静态页面的 post 请求, 查看用户是否登录, 如果登录,则获取购物车数目"""
        user = request.user
        if user.is_authenticated:
            username = user.username
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)
            return JsonResponse({"res": 1, 'username': username, 'cart_num': cart_num})
        return JsonResponse({"res": 0})


# /goods/商品id
class DetailView(View):
    """详情页"""
    def get(self, request, goods_id):
        """显示详情页"""
        # 从数据库中查取相关数据
        # 判断商品是否存在
        try:
           sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(render("goods:index"))  # 商品不存在,则返回首页
        types = GoodsType.objects.all()  # 获取所有的分类信息
        sku_comments = OrderGoods.objects.filter(sku=sku).exclude(comment="")  # 获取商品的评论信息
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
            coon = get_redis_connection("default")
            history_key = "history_%d" % user.id
            coon.lrem(history_key, 0, sku.id)  # 确保没有重复的浏览记录
            coon.lpush(history_key, sku.id)  # 从左侧插入数据
            coon.ltrim(history_key, 0, 10)  # 只保留 10 条浏览记录

        content_text = {
            'sku': sku,
            'types': types,
            'sku_comments': sku_comments,
            'same_spus': same_spus,
            'new_skus': new_skus,
            'cart_num': cart_num,
        }

        return render(request, "detail.html", content_text)


# /list/种类id/页码?sort=排序方式
class ListView(View):
    """列表页"""
    def get(self, request, type_id, page):
        """返回列表页面"""
        # 获取商品种类信息,如果不存在,则返回首页
        try:
            goods_type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse("goods:index"))

        # 获取所有商品分类信息
        types = GoodsType.objects.all()

        # 获取同一种类下所有的商品信息, 按照相应的方法进行排序
        sort = request.GET.get('sort')
        # sort: default, price, hot
        skus = GoodsSKU.objects.filter(type=goods_type)
        if sort == "price":
            skus = skus.order_by("price")
        elif sort == "hot":
            skus = skus.order_by("-sales")
        else:
            skus = skus.order_by("-id")
            sort = "default"

        # 获取新品信息
        new_skus = GoodsSKU.objects.filter(type=goods_type).order_by("-create_time")[:2]

        # 获取购物车相关信息
        user = request.user
        cart_num = 0
        if user.is_authenticated:
            # 用户登录后,则获取购物车的数目
            conn = get_redis_connection("default")
            cart_key = "cart_%d" % user.id
            cart_num = conn.hlen(cart_key)

        # 分页相关
        paginator = Paginator(skus, 3)  # Show 3 contacts per page
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)

        # 控制商品显示的页码数量,最多只显示 5 页
        page = current_page.number
        total_page = paginator.num_pages
        if total_page < 5:
            page_range = range(1, total_page + 1)
        elif page < 3:
            page_range = range(1, 6)
        elif page > total_page - 2:
            page_range = range(total_page - 4, total_page + 1)
        else:
            page_range = range(page - 2, page + 3)

        # 组织模板上下文
        content_text = {
            "type": goods_type,
            "types": types,
            "new_skus": new_skus,
            "cart_num": cart_num,
            "current_page": current_page,
            "sort": sort,
            "page_range": page_range,
        }

        return render(request, "list.html", content_text)

