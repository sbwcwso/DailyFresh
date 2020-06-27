from django.contrib import admin
from django.core.cache import cache

from goods.models import (
    GoodsType, GoodsSKU, GoodsImage, IndexPromotionBanner,
    IndexGoodsBanner, Goods, IndexTypeGoodsBanner,
)


class BaseModelAdmin(admin.ModelAdmin):
    """
    修改模型时更新静态页面
    """
    def save_model(self, request, obj, form, change):
        """
        新增或更新表中的数据时,重新生成静态文件
        """
        super().save_model(request, obj, form, change)

        # 如果在头部导入，会因为循环导入而报错
        from celery_task.tasks import generate_static_index_html
        # 发出任务,重新生成首页地址
        generate_static_index_html.delay()
        # 清除缓存, 然后访问视图时会更新缓存中的数据
        cache.delete("index_page_data")

    def delete_model(self, request, obj):
        """
        删除文件时调用的方法
        """
        super().delete_model(request, obj)

        # 如果在头部导入，会因为循环导入而报错
        from celery_task.tasks import generate_static_index_html
        # 发出任务,重新生成首页地址
        generate_static_index_html.delay()
        # 清除缓存
        cache.delete("index_page_data")


class GoodsTypeAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    list_display = ["index", "sku"]


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    list_display = ["id", "type", "sku"]


admin.site.register(GoodsImage)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsSKU)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(Goods)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)

