from django.shortcuts import render
from apps.crawler.models import Phone_brand, Phone_sku
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
    res = {'code': 200, 'data': {'xAxis': [], 'series': []}}
    # 获取手机中评论数最多的前10个品牌
    phones = Phone_sku.objects.order_by('-comments_num')[:10]

    for phone in phones:
        res['data']['xAxis'].append(phone.name)
        res['data']['series'].append(phone.comments_num)
    return res


class Echarts(View):
    def get(self, request):
        phone_cmt = cache_handler('phone_cmt', get_phone_cmt, 30)
        logger.debug(f"{phone_cmt=}")
        return JsonResponse(phone_cmt, safe=False)
