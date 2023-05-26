#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/26
import requests
from zol_phone.settings import SCRAPYD_URL

from loguru import logger

from json import dumps as json_dumps


def req_decorator(func):
    err_return = {
        "status": 0,
        "msg"   : "请求失败"
    }

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return err_return

    return wrapper


@req_decorator
def get_status():
    # 获取状态
    url = f"{SCRAPYD_URL}/daemonstatus.json"
    res = requests.get(url)
    return res.json()


@req_decorator
def get_project_list():
    # 获取项目列表
    url = f"{SCRAPYD_URL}/listprojects.json"
    res = requests.get(url)
    return res.json()


@req_decorator
def get_spider_list(project):
    # 获取项目下已发布的爬虫列表
    url = f"{SCRAPYD_URL}/listspiders.json?project={project}"
    res = requests.get(url)
    return res.json()


@req_decorator
def spider_list_ver(project):
    # 获取项目下已发布的爬虫版本列表
    url = f"{SCRAPYD_URL}/listversions.json?project={project}"
    res = requests.get(url)
    return res.json()


@req_decorator
def get_spider_status(spider):
    # 获取爬虫运行状态
    url = f"{SCRAPYD_URL}/listjobs.json?project={spider}"
    res = requests.get(url)
    return res.json()


from loguru import logger


@logger.catch
@req_decorator
def start_spider(project, spider, kwargs=None):
    # 运行一个爬虫
    url = f"{SCRAPYD_URL}/schedule.json"
    data = {
        "project": project,
        "spider" : spider,
    }
    if kwargs:
        data["data"] = kwargs
    res = requests.post(url, data=data)
    return res.json()


@req_decorator
def del_spider(project, version):
    # 删除某一版本爬虫
    url = f"{SCRAPYD_URL}/delversion.json"
    data = {
        "project": project,
        "version": version,
    }
    res = requests.post(url, data=data)
    return res.json()


@req_decorator
def del_pro(project):
    # 删除项目。注意：删除之前需要停止爬虫，才可以再次删除
    url = f"{SCRAPYD_URL}/delproject.json"
    data = {
        "project": project,
    }
    res = requests.post(url, data=data)
    return res.json()


@req_decorator
def get_jobs(project):
    # 获取jobs
    url = f"{SCRAPYD_URL}/listjobs.json?project={project}"
    res = requests.get(url)
    return res.json()


@req_decorator
def cancel(project, job_id):
    # 取消job
    url = f"{SCRAPYD_URL}/cancel.json"
    data = {
        "project": project,
        "job"    : job_id
    }
    res = requests.post(url, data=data)
    return res.json()


# def publish():
#     # 发布项目
#     url = f"{SCRAPYD_URL}/addversion.json"
#     data = {
#         "project": "mySpider",
#         "version": 1,
#         "egg"    : '1.egg'
#     }
#     res = requests.post(url, data=data)
#     return res.json()

if __name__ == '__main__':
    from pprint import pprint

    print(get_project_list())

    # crawl_proj = get_project_list()["projects"][0]
    # pprint(crawl_proj, indent=4)
    # jobs = get_jobs(crawl_proj)
    # pprint(jobs, indent=4)
    # status = get_status()
    # pprint(status, indent=4)
    # spiders = get_spider_list(crawl_proj)
    # pprint(spiders, indent=4)
    # vers = spider_list_ver(crawl_proj)
    # pprint(vers, indent=4)
    # t = start_spider(crawl_proj, 'PhoneBrandSpider')
    # pprint(t, indent=4)
    # import time
    #
    # time.sleep(3)
    # spider_status = get_spider_status(crawl_proj)
    # pprint(spider_status, indent=4)
    #
    # cancel = cancel(crawl_proj, '81ed1a0d')
    # pprint(cancel, indent=4)
    """
    'phone_crawler'
    {   'finished': [   {   'end_time': '2023-05-26 15:24:06.177533',
                            'id': '47e5b9b5fb9611edadd58cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/47e5b9b5fb9611edadd58cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/47e5b9b5fb9611edadd58cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:24:01.887765'},
                        {   'end_time': '2023-05-26 15:24:26.257225',
                            'id': '54226442fb9611edb7b28cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/54226442fb9611edb7b28cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/54226442fb9611edb7b28cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:24:21.885642'},
                        {   'end_time': '2023-05-26 15:25:36.181072',
                            'id': '7de450fdfb9611edacde8cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/7de450fdfb9611edacde8cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/7de450fdfb9611edacde8cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:25:31.885215'},
                        {   'end_time': '2023-05-26 15:27:16.530945',
                            'id': 'ac2d14aafb9611edba1e8cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/ac2d14aafb9611edba1e8cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/ac2d14aafb9611edba1e8cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:26:51.884685'},
                        {   'end_time': '2023-05-26 15:29:11.686875',
                            'id': 'fd6fe4dffb9611ed840d8cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/fd6fe4dffb9611ed840d8cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/fd6fe4dffb9611ed840d8cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:29:06.885691'},
                        {   'end_time': '2023-05-26 15:29:41.054349',
                            'id': '0e6fe24cfb9711ed8acb8cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/0e6fe24cfb9711ed8acb8cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/0e6fe24cfb9711ed8acb8cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:29:36.884546'},
                        {   'end_time': '2023-05-26 15:32:06.067329',
                            'id': '66bd8918fb9711edaa038cc681ed1a0d',
                            'items_url': '/items/phone_crawler/PhoneBrandSpider/66bd8918fb9711edaa038cc681ed1a0d.jl',
                            'log_url': '/logs/phone_crawler/PhoneBrandSpider/66bd8918fb9711edaa038cc681ed1a0d.log',
                            'project': 'phone_crawler',
                            'spider': 'PhoneBrandSpider',
                            'start_time': '2023-05-26 15:32:01.886946'}],
        'node_name': 'Leo-LPT',
        'pending': [],
        'running': [],
        'status': 'ok'}
    {   'finished': 7,
        'node_name': 'Leo-LPT',
        'pending': 0,
        'running': 0,
        'status': 'ok'}
    {   'node_name': 'Leo-LPT',
        'spiders': ['PhoneBrandSpider', 'zol', '\x1b[0m'],
        'status': 'ok'}
    {   'node_name': 'Leo-LPT',
        'status': 'ok',
        'versions': ['1685085314', '1685085349']}
    {   'jobid': '9492fddcfb9711eda8d58cc681ed1a0d',
        'node_name': 'Leo-LPT',
        'status': 'ok'}
    
    """
