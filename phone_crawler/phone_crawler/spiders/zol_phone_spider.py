#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/22
import scrapy


class ZolSpider(scrapy.Spider):
    name = "PhoneSpider"
    allowed_domains = ["detail.zol.com.cn"]
    custom_settings = {
        # 设置使用的管道
        'ITEM_PIPELINES': {
            'phone_crawler.pipelines.BrandImagePipeline': 200,
            'phone_crawler.pipelines.MysqlPipeline': 300,
        },
    }
    start_urls = [
        f"https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_3500-100000_0_1_2_0_{_}.html"
        for _ in range(1, 20)
    ]

    def parse(self, response, **kwargs):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_list)

    def parse_page(self, response, **kwargs):
        for product in response.css('.list-box .list-item'):
            yield {
                'name' : product.css('.pro-intro a::text').get(),
                'price': product.css('.price-box .price-type::text').get(),
                'url'  : product.css('.pro-intro a::attr(href)').get(),
            }
            self.parse(response, **kwargs)

    def parse_phone_info(self, response, **kwargs):
        ...
