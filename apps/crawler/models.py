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
    name = models.CharField(max_length=255, verbose_name='品牌名称', primary_key=True)
    img_url = models.CharField(max_length=255, verbose_name='品牌图片')
    img_url_s3 = models.ImageField(max_length=255, verbose_name='品牌图片local', null=True, blank=True, )
    market_share = models.FloatField(max_length=255, verbose_name='市场占有率', null=True, blank=True, )
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
    id = models.CharField(max_length=124, verbose_name='手机id', primary_key=True)
    name = models.CharField(max_length=255, verbose_name='手机名称/型号')
    intro = models.CharField(max_length=255, null=True, blank=True, verbose_name='手机简介')
    price = models.IntegerField(null=True, blank=True, verbose_name='手机价格')
    score = models.FloatField(null=True, blank=True, verbose_name='手机评分')
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name='手机详情页url')
    img_url = models.ImageField(null=True, blank=True, verbose_name='手机图片')
    comments_num = models.IntegerField(null=True, blank=True, verbose_name='手机评论数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='此条信息创建时间')

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
