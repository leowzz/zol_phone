#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/27
from django.core.cache import cache
from loguru import logger


def cache_handler(key, func, timeout=10, *args, **kwargs):
    """
    缓存处理
    :param key: 缓存键
    :param func: 数据过期后的处理函数
    :param timeout: 缓存时间
    :param args: func的参数
    :param kwargs: func的kw参数
    :return:
    """
    if cache_data := cache.get(key):
        logger.debug(f"got {key=} from cache: {cache_data=}")
        return cache_data
    cache_data = func(*args, **kwargs)
    cache.set(key, cache_data, timeout)
    logger.debug(f"set {key=} to cache: {cache_data=}")
    return cache_data
