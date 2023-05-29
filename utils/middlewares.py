#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/29
# middlewares.py

# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目中间件模块 }
# @Date: 2021/09/24 8:18
import logging

from django.db import DatabaseError
from django.http.response import JsonResponse
from django.http import HttpResponseServerError
from django.middleware.common import MiddlewareMixin
from django.shortcuts import render, redirect

from loguru import logger

from utils.enums import StatusCodeEnum
from utils.result import R
from utils.CommonException import BusinessException


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        if isinstance(exception, BusinessException):
            # 业务异常处理
            data = R.set_result(exception.enum_cls).data()
            return JsonResponse(data)

        elif isinstance(exception, DatabaseError):
            # 数据库异常
            r = R.set_result(StatusCodeEnum.DB_ERR)
            logger.error(r.data(), exc_info=True)
            return HttpResponseServerError(StatusCodeEnum.SERVER_ERR.errmsg)

        elif isinstance(exception, Exception):
            return render(request, '50x.html', context={
                          'code': '501',
                          'msg' : exception,
                          }, status=500)
            # 服务器异常处理
            r = R.server_error()
            logger.error(r.data(), exc_info=True)
            # return HttpResponseServerError(r.errmsg)
            return render(request, '50x.html', context={
                'code': r.code,
                'msg' : r.msg,
            }, status=500)

        return None
