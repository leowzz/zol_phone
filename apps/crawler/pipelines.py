# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from django.db import IntegrityError
from scrapy.exceptions import DropItem
from loguru import logger


# from apps.crawler.models import Brand


class CrawlerPipeline:
    def process_item(self, item, spider):
        # todo 将item.url存储到minio, 并将minio的url存储到item中
        # print(f"{item=}")
        return item
        # try:
        #     product = Brand(**item)
        #     product.save()
        # except IntegrityError:
        #     raise DropItem("Duplicate item found: %s" % item['name'])
        # return item


from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from apps.crawler import settings


class MyImagePipeline(ImagesPipeline, ):

    # def _get_store(self, uri: str):
    #     # 直接返回S3FilesStore对象
    #     from scrapy.pipelines.files import S3FilesStore
    #     # uri 里包含桶名和前缀, 前缀即文件夹名
    #     _store = S3FilesStore(uri=settings.IMAGES_STORE)
    #     _store.AWS_ACCESS_KEY_ID = settings.MINIO_ACCESS_KEY
    #     _store.AWS_SECRET_ACCESS_KEY = settings.MINIO_SECRET_KEY
    #     _store.AWS_ENDPOINT_URL = settings.MINIO_URI
    #     _store.AWS_REGION_NAME = settings.MINIO_REGION
    #     _store.AWS_USE_SSL = False if settings.MINIO_SCHEME == "http" else True
    #     print(f"{_store=}")
    #     return _store

    def get_media_requests(self, item, info):
        img_url = item.get("img")
        yield Request(img_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        # print(f"{request=}")
        # print(f"{response=}")
        # print(f"{info=}")
        # print(f"{item=}")
        return request.meta['item']['name'] + '.jpg'

    def item_completed(self, results, item, info):
        # print(f"{results=}")
        # print(f"{item=}")
        # print(f"{info=}")
        images = [x for ok, x in results if ok]
        print(f"{images=}")
        return item
