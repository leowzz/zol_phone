#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/29
from utils.enums import StatusCodeEnum


class R(object):
    """
    统一返回结果
    """

    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        self.data = dict() if data is None else data

    @staticmethod
    def ok(msg=None, data=None):
        return R(
            StatusCodeEnum.OK.code,
            StatusCodeEnum.OK.errmsg if msg is None else msg,
            data
        )

    @staticmethod
    def error(msg=None, data=None):
        return R(
            StatusCodeEnum.ERROR.code,
            StatusCodeEnum.ERROR.errmsg if msg is None else msg,
            data
        )

    @staticmethod
    def server_error(msg=None, data=None):
        return R(
            StatusCodeEnum.SERVER_ERROR.code,
            StatusCodeEnum.SERVER_ERROR.errmsg if msg is None else msg,
            data
        )

    @staticmethod
    def set_result(code, msg=None, data=None):
        return R(code, msg, data)

    def data(self, key, value):
        self.data[key] = value
        return self
