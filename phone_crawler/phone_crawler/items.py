# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from crawler.models import Phone_brand


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PhoneBrandItem(DjangoItem):
    django_model = Phone_brand


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()