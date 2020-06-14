from haystack import indexes

from goods.models import GoodsSKU


# 索引类名格式: 模型类名 + Index
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    对指定类的数据建立索引
    """
    # 具体根据哪些字段进行索引，定义在特定的文件中 /templates/search/indexes/goods/goodssku_text.txt
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """
        返回建立索引的模型类
        """
        return GoodsSKU

    def index_queryset(self, using=None):
        """
        建立索引的数据
        """
        return self.get_model().objects.all()
