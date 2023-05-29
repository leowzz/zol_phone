#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/29

class CommonException(Exception):
    """公共异常类"""

    def __init__(self, enum_cls):
        self.code = enum_cls.code
        self.errmsg = enum_cls.errmsg
        self.enum_cls = enum_cls  # 状态码枚举类
        super().__init__()


class BusinessException(CommonException):
    """业务异常类"""
    pass


class APIException(CommonException):
    """接口异常类"""
    pass

