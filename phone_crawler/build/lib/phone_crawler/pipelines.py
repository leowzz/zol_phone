# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from django.db import IntegrityError

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum
from loguru import logger
from hashlib import md5

from utils.minio.minio_s3 import MinioS3, get_public_url
from phone_crawler import settings


# from apps.crawler.models import Brand


class PhoneBrandPipeline:
    """
    使用mysql数据库存储品牌数据
    """

    def process_item(self, item, spider):
        item.save()
        # try:
        #     Brand.objects.create(**item)
        # except IntegrityError:
        #     pass
        return item


class BrandImagePipeline(ImagesPipeline, ):
    def get_media_requests(self, item, info):
        """
        获取图片url, 返回对应的Request对象
        """
        img_url = item.get("img_url")
        logger.debug(f"{img_url=}")
        yield Request(img_url, meta={'item': item})

    # @logger.catch()
    def file_path(self, request, response=None, info=None, *, item=None):
        """
        重写file_path方法, 用于自定义图片存储路径及文件名
        """
        _file_name = request.meta['item']['name']
        logger.debug(f"{_file_name=}")
        name_md5 = md5()  # 使用MD5加密模式
        name_md5.update(_file_name.encode('utf-8'))  # 将参数字符串传入
        name_md5 = name_md5.hexdigest()  # 获取加密串
        md5_file_name = f"{name_md5}.{request.url.split('.')[-1]}"
        logger.debug(f"{md5_file_name=}")
        return md5_file_name

    def item_completed(self, results, item, info):
        logger.info(f"item completed: {item=}")
        return item

    @logger.catch
    def image_downloaded(self, response, request, info, *, item=None):
        checksum = None
        for path, image, buf in self.get_images(response, request, info, item=item):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            self.store.persist_file(
                path,
                buf,
                info,
                meta={"width": width, "height": height},
                headers={"Content-Type": "image/jpeg"},
            )
            item["img_url_s3"] = get_public_url(path)
            logger.debug(f"{item=}")
        return checksum
