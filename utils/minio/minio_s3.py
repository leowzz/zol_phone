import os
from datetime import timedelta

from zol_phone import settings
from minio import Minio

from utils.minio.base import BaseOssClient, make_s3_key


# 获取S3的url
def get_private_url(key: str) -> str:
    """
    :param key: minio s3存储的name
    :return: url
    """
    client = MinioS3()
    return client.get_signed_url(key=key)


def get_public_url(key: str) -> str:
    url = f"{settings.MINIO_SCHEME}://{settings.MINIO_POINT_URL}/" \
          f"{settings.MINIO_BUCKET_NAME.replace('_', '-')}/{key}"
    return url


class MinioS3(BaseOssClient):

    def __new__(cls, *args, **kwargs):
        # 单例模式
        if not hasattr(cls, '_instance'):
            cls._instance = super(MinioS3, cls).__new__(cls)
        return cls._instance

    def __init__(self, bucket_name='',
                 access_key_id='',
                 secret_access_key='',
                 endpoint_url='',
                 region='',
                 is_secure: bool = None
                 ):
        self.bucket_name = bucket_name.replace("_", "-") or settings.MINIO_BUCKET_NAME.replace("_", "-")
        self.access_key_id = access_key_id or settings.MINIO_ACCESS_KEY
        self.secret_access_key = secret_access_key or settings.MINIO_SECRET_KEY
        self.endpoint_url = endpoint_url or settings.MINIO_POINT_URL
        self.region = region or settings.MINIO_REGION
        if is_secure is None:
            self.is_secure = False if settings.MINIO_SCHEME == "http" else True
        else:
            self.is_secure = is_secure
        super().__init__(bucket_name=self.bucket_name,
                         access_key_id=self.access_key_id,
                         secret_access_key=self.secret_access_key,
                         endpoint_url=self.endpoint_url,
                         region=self.region)

    @property
    def client(self):
        return Minio(
            self.endpoint_url,
            access_key=self.access_key_id,
            secret_key=self.secret_access_key,
            secure=self.is_secure,
            region=self.region
        )

    def creat_bucket(self):
        """
        创建桶
        :return:
        """
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            return True
        return False

    # 将文件传到s3的指定bucket中
    def upload_file(self, file_path, upload_path, add_suffix=True, **kwargs):
        """
        :param file_path: 本地
        :param upload_path: 远端
        :param add_suffix: 是否添加后缀
        :return:
        """
        s3_key = make_s3_key(upload_path)
        print(s3_key)
        if os.path.exists(file_path):
            self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=s3_key if add_suffix else upload_path,
                file_path=file_path,
                num_parallel_uploads=5
            )
            return get_public_url(s3_key)
        else:
            return False

    def upload_file_obj(self, file, upload_path, length, content_type, **kwargs):
        s3_key = make_s3_key(upload_path)
        print(s3_key)
        if self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=s3_key,
                data=file,
                length=length,
                content_type=content_type,
                num_parallel_uploads=5
        ):
            return s3_key
        return False

    def download_file(self, download_path, key):
        """
        下载文件
        :param download_path: 下载路径
        :param key: 文件key
        :return:
        """
        self.client.fget_object(self.bucket_name, key, download_path)
        return True, download_path

    def download_file_obj(self, key):
        data = self.client.get_object(self.bucket_name, key)
        buf = data.read()
        return True, buf

    def delete_file(self, key):
        """
        删除文件
        :param key:
        :return:
        """
        self.client.remove_object(self.bucket_name, key)
        return True

    def get_signed_url(self, key):
        if not key:
            return ''
        url = self.client.presigned_get_object(self.bucket_name, key, expires=timedelta(hours=24))
        return url

    def get_file_size(self, key):
        """
        获取文件大小
        :param key:
        :return:
        """
        stat = self.client.stat_object(self.bucket_name, key)
        return stat.size

    def get_file_info(self, key):
        """
        获取文件信息
        :param key:
        :return:
        """
        stat = self.client.stat_object(self.bucket_name, key)
        return stat

    def check_key_is_exist(self, key):
        """
        检查文件是否存在
        :param key:
        :return:
        """
        from minio.error import S3Error
        try:
            self.client.stat_object(self.bucket_name, key) is not None
        except S3Error as e:
            return False
        return True

    def get_pages(self, delimiter='/', prefix=None):
        pass

    def get_object_list(self, prefix=None):
        """
        获取文件列表
        :param prefix: 文件前缀, 例如test文件夹下的文件, 则prefix为test/
        """

        _objs = self.client.list_objects(
            self.bucket_name,
            prefix=prefix,
        )
        return _objs

    def download_dir(self, delimiter='/', prefix=None, local='/tmp'):
        pass


if __name__ == '__main__':
    minio = MinioS3()
    # 测试上传文件
    # res = minio.upload_file(r'Y:\01_Imp\Python\学习\Django\meiduo\requirement.txt', '/test/11.txt')
    # print(res)

    # 测试下载文件
    # res = minio.download_file(r'Y:\01_Imp\Python\学习\requirement.txt', 'test-7603583d34df4afd91fbcc668037c0a0.txt')
    # print(res)

    # 测试删除文件
    # res = minio.delete_file('test-7603583d34df4afd91fbcc668037c0a0.txt')
    # print(res)

    # 测试文件是否存在
    # print(minio.check_key_is_exist('requirement-765641aacf7e48c89ec41d9e2b4240b0.txt'))
    # print(minio.check_key_is_exist('test-7603583d34df4afd91fbcc668037c0a0.txt'))

    # 测试获取文件列表
    # li = minio.get_object_list()
    # print(li)
    # for i in li:
    #     print(i.object_name)
    #     print(i.size)
    #     print(i.is_dir)
    #     print()
