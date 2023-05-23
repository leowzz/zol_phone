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
    from loguru import logger
    @logger.catch
    def image_downloaded(self, response, request, info, *, item=None):
        from utils.minio.minio_s3 import MinioS3, get_public_url
        from scrapy.utils.misc import md5sum
        minio = MinioS3()
        checksum = None
        for path, image, buf in self.get_images(response, request, info, item=item):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            buf.seek(0)
            s3_key = minio.upload_file_obj(
                upload_path=path,
                file=buf,
                length=buf.getbuffer().nbytes,
                content_type=f"image/{image.format.lower() if image.format else 'jpeg'}",
            )
            item['img_local'] = get_public_url(s3_key)
            print(f"{item=}")
        return checksum

    def get_media_requests(self, item, info):
        """
        重写get_media_requests方法, 用于下载图片
        """
        img_url = item.get("img_url")
        yield Request(img_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        重写file_path方法, 用于自定义图片存储路径
        """
        return f"{settings.IMAGES_DIR}/{request.meta['item']['name']}.jpg"

    def item_completed(self, results, item, info):
        # print(f"{results=}")
        # print(f"{item=}")
        # print(f"{info=}")
        images = [x for ok, x in results if ok]
        # print(f"{images=}")
        return item
