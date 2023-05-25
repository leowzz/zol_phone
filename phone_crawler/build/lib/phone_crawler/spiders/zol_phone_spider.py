#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/22
import scrapy


class ZolSpider(scrapy.Spider):
    name = "zol"
    allowed_domains = ["detail.zol.com.cn"]
    start_urls = [
        "https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_3500-100000_0_1_2_0_1.html"
    ]

    def parse(self, response):
        for product in response.css('.list-box .list-item'):
            yield {
                'name' : product.css('.pro-intro a::text').get(),
                'price': product.css('.price-box .price-type::text').get(),
                'url'  : product.css('.pro-intro a::attr(href)').get(),
            }
