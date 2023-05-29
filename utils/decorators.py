#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/29
from django.shortcuts import render, HttpResponse, redirect
from loguru import logger


def resp_500(func):
    @logger.catch
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return render(args[1], '50x.html', context={
                'code': '501',
                'msg' : e,
            }, status=500)

    return wrapper
