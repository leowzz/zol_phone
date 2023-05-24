from django.db import models


class Phone_brand(models.Model):
    """
    name = scrapy.Field()  # 品牌名称
    img_url = scrapy.Field()  # 品牌图片 公网url
    img_url_s3 = scrapy.Field()  # 品牌图片 本地url
    market_share = scrapy.Field()  # 市场占有率
    feedback = scrapy.Field()  # 好评率
    price_min = scrapy.Field()  # 最低价
    price_max = scrapy.Field()  # 最高价
    phone_num = scrapy.Field()  # 机型数量
    """
    name = models.CharField(max_length=255, verbose_name='品牌名称')
    img_url = models.CharField(max_length=255, verbose_name='品牌图片')
    img_url_s3 = models.ImageField(max_length=255, verbose_name='品牌图片local')
    market_share = models.CharField(max_length=255, verbose_name='市场占有率')
    feedback = models.CharField(max_length=255, verbose_name='好评率')
    price_min = models.CharField(max_length=255, verbose_name='最低价')
    price_max = models.CharField(max_length=255, verbose_name='最高价')
    phone_num = models.CharField(max_length=255, verbose_name='机型数量')

    def __str__(self):
        return self

    class Meta:
        db_table = 'phone_brand'
        verbose_name = '手机品牌'
        verbose_name_plural = verbose_name


class Phone_sku(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self

    class Meta:
        db_table = 'phone_sku'
        verbose_name = '手机基本信息'
        verbose_name_plural = verbose_name

# class SPU(models.Model):
#     """商品SPU"""
#     name = models.CharField(max_length=50, verbose_name='名称')
#     brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
#     category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name='一级类别')
#     category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat2_spu', verbose_name='二级类别')
#     category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat3_spu', verbose_name='三级类别')
#     sales = models.IntegerField(default=0, verbose_name='销量')
#     comments = models.IntegerField(default=0, verbose_name='评价数')
#     desc_detail = models.TextField(default='', verbose_name='详细介绍')
#     desc_pack = models.TextField(default='', verbose_name='包装信息')
#     desc_service = models.TextField(default='', verbose_name='售后服务')
#
#     class Meta:
#         db_table = 'phone_spu'
#         verbose_name = '手机详细信息SPU'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
