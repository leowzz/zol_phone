from django.db import models


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


class Brand(BaseModel):
    """品牌"""
    name = models.CharField(max_length=20, verbose_name='名称')
    logo = models.ImageField(verbose_name='Logo图片')
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母')

    class Meta:
        db_table = 'phone_brand'
        verbose_name = '手机厂商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPU(BaseModel):
    """商品SPU"""
    name = models.CharField(max_length=50, verbose_name='名称')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name='一级类别')
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat2_spu', verbose_name='二级类别')
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat3_spu', verbose_name='三级类别')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数')
    desc_detail = models.TextField(default='', verbose_name='详细介绍')
    desc_pack = models.TextField(default='', verbose_name='包装信息')
    desc_service = models.TextField(default='', verbose_name='售后服务')

    class Meta:
        db_table = 'phone_spu'
        verbose_name = '手机详细信息SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
