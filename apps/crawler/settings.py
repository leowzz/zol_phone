import os.path

import django

# django.setup()
# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "crawler"

SPIDER_MODULES = ["apps.crawler.spiders"]
NEWSPIDER_MODULE = "apps.crawler.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "crawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',

import os
from zol_phone.settings import *

LOG_LEVEL = 'INFO'

# 图片本地下载路径
# IMAGES_STORE = os.path.abspath('images')
IMAGES_STORE = f's3://{AWS_BUCKET_NAME}/{IMAGES_DIR}/'

# 图片过期时间, 90天内 抓取的都不会被重抓
IMAGES_EXPIRES = 90

ITEM_PIPELINES = {
    'apps.crawler.pipelines.BrandImagePipeline': 200,
    'apps.crawler.pipelines.PhoneBrandPipeline': 300,
}
