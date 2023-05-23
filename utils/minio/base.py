import uuid


def make_s3_key(file_name: str, dir_: str = '/') -> str:
    """
    构建s3 key(完整)
    :param file_name:
    :param dir_:
    :return:
    """
    import os.path
    prefix, suffix = os.path.splitext(file_name)
    if not all([prefix, suffix]):
        raise ValueError('Please enter a valid file name')
    key = f'{prefix}-{uuid.uuid4().hex}{suffix}'
    return key


class BaseOssClient(object):
    def __init__(self,
                 bucket_name='',
                 access_key_id='',
                 secret_access_key='',
                 endpoint_url='',
                 region=''
                 ):
        self.bucket_name = bucket_name.replace("_", "-")
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.endpoint_url = endpoint_url
        self.region = region

    @property
    def client(self):
        raise NotImplementedError()

    # 将文件传到s3的指定bucket中
    def upload_file(self, file_path, upload_path, add_suffix=True, **kwargs):
        """
        :param file_path: 对应s3存储的位置
        :param upload_path: 文件的上传位置
        :param add_suffix: 是否添加后缀
        :return:
        """
        raise NotImplementedError()

    def upload_file_obj(self, file, upload_path, length, content_type, **kwargs):
        """
        上传文件对象, file: An object having callable read() returning bytes object.
        """
        raise NotImplementedError()

    def get_signed_url(self, key):
        """
        签名
        :param key:
        :return:
        """
        raise NotImplementedError()

    def download_file(self, download_path, key):
        """
        下载文件到本地
        :param download_path:
        :param key:
        :return:
        """
        raise NotImplementedError()

    def download_file_obj(self, key):
        """
        下载文件到buffer
        :param key:
        :return:
        """
        raise NotImplementedError()

    def delete_file(self, key):
        """
        删除文件
        :param key:
        :return:
        """
        raise NotImplementedError()

    def check_key_is_exist(self, key):
        """
        判断文件是否存在
        :param key:
        :return:
        """
        raise NotImplementedError()

    def get_pages(self, delimiter='/', prefix=None):
        """
        分页
        :param delimiter:
        :param prefix:
        :return:
        """
        raise NotImplementedError()

    def get_object_list(self, prefix=None):
        """
        获取所有文件
        :param prefix:
        :return:
        """
        raise NotImplementedError()

    def download_dir(self, delimiter='/', prefix=None, local='/tmp'):
        """
        下载整个文件夹
        :param delimiter:
        :param prefix:
        :param local:
        :return:
        """
        raise NotImplementedError()

    def creat_bucket(self):
        """
        创建桶
        :return:
        """
        raise NotImplementedError()


if __name__ == '__main__':
    s3_key_ = make_s3_key('test.txt')
    print(s3_key_)
