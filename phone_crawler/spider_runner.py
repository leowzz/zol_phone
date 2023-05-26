#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/26
from phone_crawler.spiders.phone_brand_spider import PhoneBrandSpider

from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(PhoneBrandSpider)
process.start()
