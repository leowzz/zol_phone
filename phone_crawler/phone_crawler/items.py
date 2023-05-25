# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PhoneBrandItem(scrapy.Item):
    name = scrapy.Field()  # 品牌名称
    img_url = scrapy.Field()  # 品牌图片 公网url
    img_url_s3 = scrapy.Field()  # 品牌图片 本地url
    market_share = scrapy.Field()  # 市场占有率
    feedback = scrapy.Field()  # 好评率
    price_min = scrapy.Field()  # 最低价
    price_max = scrapy.Field()  # 最高价
    phone_num = scrapy.Field()  # 机型数量


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
