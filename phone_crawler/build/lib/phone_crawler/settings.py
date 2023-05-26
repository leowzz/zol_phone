# Scrapy settings for phone_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "phone_crawler"

SPIDER_MODULES = ["phone_crawler.spiders"]
NEWSPIDER_MODULE = "phone_crawler.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "phone_crawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "phone_crawler.middlewares.PhoneCrawlerSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "phone_crawler.middlewares.PhoneCrawlerDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "phone_crawler.pipelines.PhoneCrawlerPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = 'DEBUG'
# LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'phone_crawler.pipelines.BrandImagePipeline': 200,
    'phone_crawler.pipelines.MysqlPipeline': 300,
}

# 使用Minio作为S3对象存储
MINIO_ACCESS_KEY = AWS_ACCESS_KEY_ID = 'cxizCwezI4OqnCbf'
MINIO_SECRET_KEY = AWS_SECRET_ACCESS_KEY = 'Zvt2hShnCKWRq6jyAgtCg8p11OBC89fc'
MINIO_REGION = AWS_REGION_NAME = 'us-east-1'
MINIO_SCHEME = AWS_SCHEME = 'http'
MINIO_BUCKET_NAME = AWS_BUCKET_NAME = 'zol.phone'
MINIO_POINT_URL = 'cent:9090'
AWS_ENDPOINT_URL = f"{MINIO_SCHEME}://{MINIO_POINT_URL}"
AWS_URI = f"s3://{MINIO_BUCKET_NAME}"
AWS_USE_SSL = False
IMAGES_DIR = "images"
# 图片本地下载路径
# IMAGES_STORE = os.path.abspath('images')
IMAGES_STORE = f's3://{AWS_BUCKET_NAME}/{IMAGES_DIR}/'

# 图片过期时间, 90天内抓取的都不会重复存储
IMAGES_EXPIRES = 0

import sys
import os

# 为了能够在scrapy中使用django的model
sys.path.append('../../zol_phone')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO_ROOT = os.path.dirname(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'zol_phone.settings'

import django

django.setup()
