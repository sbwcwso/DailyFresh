from django.contrib import admin
from goods.models import GoodsType, GoodsSKU, GoodsImage, IndexPromotionBanner,\
    IndexGoodsBanner, Goods, IndexTypeGoodsBanner
from celery_task.tasks import generate_static_index_html
from django.core.cache import cache


class BaseModelAdmin(admin.ModelAdmin):
    """修改模型时更新静态页面"""
    def save_model(self, request, obj, form, change):
        """新增或更新表中的数据时,重新生成静态文件"""
        super().save_model(request, obj, form, change)

        # 发出任务,重新生成首页地址
        generate_static_index_html.delay()
        # 清除缓存
        cache.delete("index_page_data")

    def delete_model(self, request, obj):
        """删除文件时调用的方法"""
        super().delete_model(request, obj)

        # 发出任务,重新生成首页地址
        generate_static_index_html.delay()
        # 清除缓存
        cache.delete("index_page_data")


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    list_display = ["index", "sku"]


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    list_display = ["id", "type", "sku"]

# Register your models here.


admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(Goods)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
