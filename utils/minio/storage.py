#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/7

from django.core.files.storage import Storage
from utils.minio.minio_s3 import MinioS3
from zol_phone.settings import MINIO_POINT_URL


class MinioStorage(Storage):

    def __init__(self):
        self.minio = MinioS3()

    def url(self, name):
        return rf"http://{MINIO_POINT_URL}/{name}"

    def open(self, name, mode='rb'):
        """Retrieve the specified file from storage."""
        ...

    def save(self, name, content, max_length=None):
        ...

    def path(self, name):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    def get_modified_time(self, name):
        pass
