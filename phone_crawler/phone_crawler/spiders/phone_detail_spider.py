#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/26
import scrapy
from phone_crawler.items import Phone_SKU
from loguru import logger
from apps.crawler.models import Phone_sku


class PhoneDetail(scrapy.Spider):
    name = "PhoneDetailSpider"
    allowed_domains = ["detail.zol.com.cn"]
    custom_settings = {
        # 设置使用的管道
        'ITEM_PIPELINES': {
            # 'phone_crawler.pipelines.BrandImagePipeline': 200,
            # 'phone_crawler.pipelines.MysqlPipeline'     : 300,
        },
    }
    # 从数据库中获取所有的手机型号的详情页链接
    start_urls = Phone_sku.objects.all().values_list('url', flat=True)

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

    def parse_detail(self, response, **kwargs):
        # 解析手机详情页
        pass
    # @logger.catch
    # def parse_page(self, response, **kwargs):
    #     # 爬取手机列表页
    #     # 爬取class为pic-mode-box的div下的所有包含data-follow-id属性的li标签
    #     for product in response.css('.pic-mode-box li[data-follow-id]'):
    #         item = Phone_SKU()
    #         item['id'] = product.css('li::attr(data-follow-id)').get()
    #         _name = product.css('li h3 a::text').get().strip()
    #         item['name'] = _name.strip() if _name else None
    #         item['intro'] = product.css('li h3 a span::text').get()
    #         _price = product.css('.price-type::text').get()
    #         item['price'] = _price if _price != '暂无报价' else None
    #         item['score'] = product.css('.score::text').get()
    #         item['url'] = r"https://detail.zol.com.cn" + product.css('li a::attr(href)').get()
    #         item['img_url'] = product.css('img').re_first(r'src="(.+?)"')
    #         comments_num = product.css('.comment-num::text').re_first(r'\d+')
    #         item['comments_num'] = comments_num if comments_num else '0'
    #         item['created_at'] = product.css('.date::text').get()
    #         yield item


