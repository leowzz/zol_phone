from django.shortcuts import render
from apps.crawler.models import Phone_brand, Phone_sku, Phone_spu
from django.views import View
from loguru import logger
from django.http import JsonResponse
from utils.cacher import cache_handler


# Create your views here.
def get_brands_():
    res = {
        'code'     : 200, 'brand_pst': [],
        'phone_num': {'name': [], 'num': []},
        'good_pst' : {'name': [], 'feedback': []}
    }
    # 市场占有率
    brand_pst = Phone_brand.objects.order_by('-market_share')
    for brand in brand_pst:
        res['brand_pst'].append({
            'name' : brand.name,
            'value': brand.market_share,
        })
    # 手机数量
    brand_num = Phone_brand.objects.order_by('-phone_num')[:20]
    for brand in brand_num:
        res['phone_num']['name'].append(brand.name)
        res['phone_num']['num'].append(brand.phone_num)
    # 好评率
    brand_price = Phone_brand.objects.order_by('-feedback')[:20]
    for brand in brand_price:
        res['good_pst']['name'].append(brand.name)
        res['good_pst']['feedback'].append(brand.feedback)
    return res


class BrandView(View):
    # @logger.catch
    def get(self, request):
        # 获取所有品牌名称及市场占有率
        # 缓存处理
        cache_brands = cache_handler('brands_pst_fdbk_num', get_brands_, 30)
        logger.debug(f"{cache_brands=}")
        return JsonResponse(cache_brands, safe=False)


def get_phone_cmt():
    res = {'code': 200, }
    for name in ['cmt', 'price', 'score', 'jd_price']:
        res[name] = {'xAxis': [], 'series': []}
    # 获取手机中评论数最多的前10个品牌
    phone_cmt = Phone_sku.objects.order_by('-comments_num')[:15]
    # 获取价格最高的前10个手机
    phone_price = Phone_sku.objects.order_by('-price')[:12]
    # 获取手机中评分最高的前10个手机
    phone_score = Phone_sku.objects.order_by('-score')[:15]
    # 获取手机详细信息中京东售价前十的手机
    phone_jd_price = Phone_spu.objects.order_by('-mall_price')[:12]

    for phone in phone_cmt:
        res['cmt']['xAxis'].append(phone.name)
        res['cmt']['series'].append(phone.comments_num)
    for phone in phone_price:
        res['price']['xAxis'].append(phone.name)
        res['price']['series'].append(phone.price)
    for phone in phone_score:
        res['score']['xAxis'].append(phone.name)
        res['score']['series'].append(phone.score)
    for phone in phone_jd_price:
        res['jd_price']['xAxis'].append(phone.name)
        res['jd_price']['series'].append(phone.mall_price)
    return res


class Echarts(View):
    def get(self, request):
        phone_cmt = cache_handler('phone_:cmt:price:score', get_phone_cmt, 30)
        logger.debug(f"{phone_cmt=}")
        return JsonResponse(phone_cmt, safe=False)
