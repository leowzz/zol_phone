#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/26
import scrapy
from phone_crawler.items import PhoneSpuItem
from loguru import logger
from apps.crawler.models import Phone_sku
import json
import datetime


class PhoneDetail(scrapy.Spider):
    name = "PhoneDetailSpider"
    allowed_domains = ["detail.zol.com.cn"]
    custom_settings = {
        # 设置使用的管道
        'ITEM_PIPELINES': {
            'phone_crawler.pipelines.BrandImagePipeline': 200,
            'phone_crawler.pipelines.MysqlPipeline'     : 300,
        },
    }
    # 从数据库中获取所有的手机型号的详情页链接
    start_urls = Phone_sku.objects.all().values_list('url', flat=True)

    @logger.catch
    def parse(self, response, **kwargs):
        # 先爬取手机信息页
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.get_detail)

    def get_detail(self, response, **kwargs):
        # 获取手机详情页链接
        detail_url = response.css('.section-more::attr(href)').get()
        detail_url = r"https://detail.zol.com.cn" + detail_url
        # 爬取手机详情页
        yield scrapy.Request(detail_url, callback=self.parse_detail)

    @logger.catch
    def parse_detail(self, response, **kwargs):
        # 解析手机详情页
        item = PhoneSpuItem()
        breadcrumb_a = response.css('.breadcrumb a[target]')
        _id = breadcrumb_a.re_first(r'(\d+).shtml') if breadcrumb_a else None
        if not Phone_sku.objects.filter(id=_id).exists() and breadcrumb_a:
            __id = None
        item['_id'] = _id
        item['name'] = breadcrumb_a.css('a::text').get()
        item['url'] = r"https://detail.zol.com.cn" + breadcrumb_a.css('a::attr(href)').get()
        item['img_url'] = response.css('.big-pic-fl a img::attr(src)').get()
        item['last_modify'] = datetime.datetime.now()
        _price = response.css('#param-list-b2c-jd::text')
        item['mall_price'] = _price.re_first(r"\d+") if _price else None
        tables = response.css('.detailed-parameters table')
        # 详情页的表格
        detail_table_names = ['basic_info', 'outline', 'hardware', 'screen', 'camera', 'network', 'battery']
        for i in range(len(detail_table_names)):
            table_detail = tables[i]
            basic_info = {}
            for tr in table_detail.css('table tr'):
                basic_info[f"{tr.css('th span::text').get()}"] = tr.css('td span::text').get()
            item[detail_table_names[i]] = json.dumps(basic_info, ensure_ascii=False)

        logger.debug(item)
        yield item
