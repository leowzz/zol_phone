from django.shortcuts import render
from apps.crawler.models import Phone_brand, Phone_sku, Phone_spu
from django.views import View
from loguru import logger
from django.http import JsonResponse
from utils.cacher import cache_handler


# Create your views here.
def get_brands_pst():
    res = []
    brands = Phone_brand.objects.all()
    for brand in brands:
        res.append({
            'name'        : brand.name,
            'market_share': brand.market_share,
        })
    return res


class BrandView(View):
    # @logger.catch
    def get(self, request):
        # 获取所有品牌名称及市场占有率
        # 缓存处理
        cache_brands = cache_handler('brands_pst', get_brands_pst, 30 * 12 * 60 * 60)
        logger.debug(f"{cache_brands=}")
        return JsonResponse(cache_brands, safe=False)


def get_phone_cmt():
    res = {'code': 200, }
    for name in ['cmt', 'price', 'score', 'jd_price']:
        res[name] = {'xAxis': [], 'series': []}
    # 获取手机中评论数最多的前10个品牌
    phone_cmt = Phone_sku.objects.order_by('-comments_num')[:10]
    # 获取价格最高的前10个手机
    phone_price = Phone_sku.objects.order_by('-price')[:10]
    # 获取手机中评分最高的前10个手机
    phone_score = Phone_sku.objects.order_by('-score')[:10]
    # 获取手机详细信息中京东售价前十的手机
    phone_jd_price = Phone_spu.objects.order_by('-mall_price')[:10]

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
