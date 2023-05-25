#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/23
import scrapy
from loguru import logger
from phone_crawler.items import PhoneBrandItem
from twisted.internet import task, reactor
import requests


class PhoneBrandSpider(scrapy.Spider):
    name = 'PhoneBrandSpider'
    custom_settings = {
        # 设置使用的管道
        'ITEM_PIPELINES': {
            # 'apps.crawler.pipelines.BrandImagePipeline': 200,
            'phone_crawler.pipelines.PhoneBrandPipeline': 300,
        },
    }
    allowed_domains = [
        "detail.zol.com.cn",
        "mobile.zol.com.cn",
    ]
    start_urls = [
        # "https://mobile.zol.com.cn/manu_list.html",
        # "https://top.zol.com.cn/compositor/57/manu_attention.html",
        # "http://localhost:8080/brands.html",
        "http://localhost:8080/phone_brand_rank_list.html",

    ]


    @logger.catch
    def parse(self, response):
        for product in response.css('.rank-list__item'):
            item = PhoneBrandItem()
            item['name'] = product.css('.cell-2 p a::text').get().strip()
            item['img_url'] = product.css('.cell-2 img::attr(src)').get()
            item['img_url_s3'] = None
            market_share = product.css('.cell-4::text').re_first(r'\d+\.\d+')
            item['market_share'] = market_share if market_share != '-' else '0'
            item['feedback'] = product.css('.cell-6::text').extract_first().strip().replace('%', '')
            price_range = product.css('.rank__price::text').re_first(r'\d+\-\d+')
            item['price_min'], item['price_max'] = price_range.split('-') if price_range else ('0', '0')
            item['phone_num'] = product.css('.rank__price span::text').re_first(r'共(\d+)款')
            logger.debug(f"parse: {item=}")
            yield item

    def parse_image(self, response):
        print(f"{response=}")


# @logger.catch
# def main():
#     from scrapy.crawler import CrawlerProcess
#     from scrapy.utils.project import get_project_settings
#
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(PhoneBrandSpider)
#     process.start()


if __name__ == '__main__':
    # main()
    ...
