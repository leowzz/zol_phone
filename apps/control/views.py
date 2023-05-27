from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from apps.crawler.utils import get_project_list, get_spider_list
from zol_phone.settings import BASE_DIR, SCRAPYD_PROJECT_NAME

import os
from loguru import logger
from apps.crawler.models import Phone_sku, Phone_brand, Phone_spu


# Create your views here.

class IndexView(View):
    def get(self, request):
        return redirect('/static/index.html')


@logger.catch
@xframe_options_exempt
def home_page(request):
    # 获取手机信息数
    phone_info_cnt = Phone_sku.objects.all().count()
    phone_detail_cnt = Phone_spu.objects.all().count()
    brand_info_cnt = Phone_brand.objects.all().count()
    # 获取数据条数
    data_cnt = sum([phone_info_cnt, phone_detail_cnt, brand_info_cnt])
    # 获取爬虫信息
    proj_names = [_ for _ in get_project_list()['projects'] if _ != 'default']
    spider_cnt = 0
    for proj_name in proj_names:
        spider_cnt += len(get_spider_list(proj_name)['spiders'])
    # 获取日志条数
    log_cnt = 0
    log_path = os.path.join(BASE_DIR, SCRAPYD_PROJECT_NAME, 'logs')
    for root, dirs, files in os.walk(log_path):
        for file in files:
            if file.endswith('.log'):
                log_cnt += 1
    return render(request, 'home_page.html', context={
        'data_cnt'  : data_cnt,
        'phone_cnt' : phone_info_cnt,
        'spider_cnt': spider_cnt,
        'log_cnt'   : log_cnt,
    })
