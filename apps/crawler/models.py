from django.db import models
from utils.models import BaseModel


class Phone_brand(models.Model):
    name = models.CharField(max_length=255, verbose_name='品牌名称', primary_key=True)
    img_url = models.CharField(max_length=255, verbose_name='品牌图片')
    img_url_s3 = models.ImageField(max_length=255, verbose_name='品牌图片local', null=True, blank=True, )
    market_share = models.FloatField(verbose_name='市场占有率', null=True, blank=True, )
    feedback = models.FloatField(verbose_name='好评率')
    price_min = models.IntegerField(verbose_name='最低价')
    price_max = models.IntegerField(verbose_name='最高价')
    phone_num = models.IntegerField(verbose_name='机型数量')

    def __str__(self):
        return self.name

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
    img_url = models.ImageField(max_length=255, null=True, blank=True, verbose_name='手机图片')
    img_url_s3 = models.ImageField(max_length=255, null=True, blank=True, verbose_name='手机图片s3存储url')
    comments_num = models.IntegerField(null=True, blank=True, verbose_name='手机评论数')
    last_modify = models.DateTimeField(auto_now_add=True, verbose_name='此条信息最后更新时间', null=True, blank=True, )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'phone_sku'
        verbose_name = '手机基本信息'
        verbose_name_plural = verbose_name


class Phone_spu(models.Model):
    _id = models.CharField(max_length=124, verbose_name='手机id', primary_key=True)
    name = models.CharField(max_length=255, verbose_name='手机名称/型号')
    url = models.CharField(max_length=255, verbose_name='页面url')
    img_url = models.ImageField(max_length=255, null=True, blank=True, verbose_name='手机图片')
    img_url_s3 = models.ImageField(max_length=255, null=True, blank=True, verbose_name='手机图片s3存储url')
    last_modify = models.DateTimeField(auto_now_add=True, verbose_name='此条信息最后更新时间', null=True, blank=True, )
    mall_price = models.IntegerField(null=True, blank=True, verbose_name='商城价格')
    # 详细参数
    basic_info = models.TextField(null=True, blank=True, verbose_name='基本信息, json格式')
    outline = models.TextField(null=True, blank=True, verbose_name='外形, json格式')
    hardware = models.TextField(null=True, blank=True, verbose_name='硬件, json格式')
    screen = models.TextField(null=True, blank=True, verbose_name='屏幕, json格式')
    camera = models.TextField(null=True, blank=True, verbose_name='摄像头, json格式')
    network = models.TextField(null=True, blank=True, verbose_name='网络, json格式')
    battery = models.TextField(null=True, blank=True, verbose_name='电池, json格式')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'phone_detail'
        verbose_name = '手机详细参数'
        verbose_name_plural = verbose_name
