from django.db import models
from utils.models import BaseModel


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


class Spider(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)  # 0:未开始 1:进行中 2:已完成
    run_times = models.IntegerField(default=0)  # 运行次数
    last_run_time = models.DateTimeField(auto_now=True)  # 最后一次运行时间

    def __str__(self):
        return self

    class Meta:
        db_table = 'spider'
        verbose_name = '爬虫'
        verbose_name_plural = verbose_name
