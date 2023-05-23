#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/23
import scrapy
from loguru import logger
from apps.crawler.items import PhoneBrandItem


class PhoneBrandSpider(scrapy.Spider):
    name = 'PhoneBrandSpider'
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
            item['img_local'] = None
            # item.name = product.css('a::text').get()
            # print(f"{item=}")
            yield item

    def parse_image(self, response):
        print(f"{response=}")


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(PhoneBrandSpider)
    process.start()
