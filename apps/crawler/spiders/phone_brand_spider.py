#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/23
import scrapy
from loguru import logger


class PhoneBrandSpider(scrapy.Spider):
    name = 'PhoneBrandSpider'
    allowed_domains = [
        "detail.zol.com.cn",
        "mobile.zol.com.cn",
    ]
    start_urls = [
        # "https://mobile.zol.com.cn/manu_list.html",
        "http://localhost:8080/brands.html"
    ]

    @logger.catch
    def parse(self, response):
        for product in response.css('.BrandsList li'):
            # print(f"{product=}")
            yield {
                # 'name' : product.css('li a::text').extract(),
                # 品牌名称 正则匹配中文
                'name': product.css('li a::text').re_first(r"[\u4e00-\u9fa5]+"),
                # 'price': product.css('.price-box .price-type::text').get(),
                'img' : product.css('li img::attr(src)').get(),
                # "image": scrapy.Request(product.css('li img::attr(src)').get(), callback=self.parse_image)
            }

    def parse_image(self, response):
        print(f"{response=}")



if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(PhoneBrandSpider)
    process.start()
