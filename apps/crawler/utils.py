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
    crawl_proj = get_project_list()["projects"][0]
    print(f"{crawl_proj=}")
    status = get_status()
    print(f"{status=}")
    spiders = get_spider_list(crawl_proj)
    print(f"{spiders=}")
    vers = spider_list_ver(crawl_proj)
    print(f"{vers=}")
    start_spider_ = start_spider(crawl_proj, 'PhoneBrandSpider')
    print(f"{start_spider_=}")
    jobs = get_jobs(crawl_proj)
    print(f"{jobs=}")
    import time

    time.sleep(10)
    jobs = get_jobs(crawl_proj)
    print(f"{jobs=}")
    cancel = cancel(crawl_proj, '81ed1a0d')
    print(f"{cancel=}")

    """
    crawl_proj='phone_crawler'
    status={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': 0, 'running': 0, 'finished': 0}
    spiders={'node_name': 'Leo-LPT', 'status': 'ok', 'spiders': ['PhoneBrandSpider', 'PhoneSpider', '\x1b[0m']}
    vers={'node_name': 'Leo-LPT', 'status': 'ok', 'versions': ['1685085314', '1685085349', '1685105067']}
    start_spider_={'node_name': 'Leo-LPT', 'status': 'ok', 'jobid': '5197dfd3fbc411eda66d8cc681ed1a0d'}
    jobs={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '5197dfd3fbc411eda66d8cc681ed1a0d'}], 'running': [], 'finished': []}
    jobs={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': [], 'running': [], 'finished': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '5197dfd3fbc411eda66d8cc681ed1a0d', 'start_time': '2023-05-26 20:53:33.227064', 'end_time': '2023-05-26 20:53:41.825362', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.jl'}]}
    cancel={'node_name': 'Leo-LPT', 'status': 'ok', 'prevstate': None}
    """
    """
    crawl_proj='phone_crawler'
    status={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': 0, 'running': 0, 'finished': 1}
    spiders={'node_name': 'Leo-LPT', 'status': 'ok', 'spiders': ['PhoneBrandSpider', 'PhoneSpider', '\x1b[0m']}
    vers={'node_name': 'Leo-LPT', 'status': 'ok', 'versions': ['1685085314', '1685085349', '1685105067']}
    start_spider_={'node_name': 'Leo-LPT', 'status': 'ok', 'jobid': '85a1742bfbc411ed94908cc681ed1a0d'}
    jobs={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '85a1742bfbc411ed94908cc681ed1a0d'}], 'running': [], 'finished': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '5197dfd3fbc411eda66d8cc681ed1a0d', 'start_time': '2023-05-26 20:53:33.227064', 'end_time': '2023-05-26 20:53:41.825362', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.jl'}]}
    jobs={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': [], 'running': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '85a1742bfbc411ed94908cc681ed1a0d', 'pid': 19404, 'start_time': '2023-05-26 20:55:03.226823'}], 'finished': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '5197dfd3fbc411eda66d8cc681ed1a0d', 'start_time': '2023-05-26 20:53:33.227064', 'end_time': '2023-05-26 20:53:41.825362', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.jl'}]}
    cancel={'node_name': 'Leo-LPT', 'status': 'ok', 'prevstate': None}
    """

    """
    crawl_proj='phone_crawler'
    status={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': 0, 'running': 0, 'finished': 2}
    spiders={'node_name': 'Leo-LPT', 'status': 'ok', 'spiders': ['PhoneBrandSpider', 'PhoneSpider', '\x1b[0m']}
    vers={'node_name': 'Leo-LPT', 'status': 'ok', 'versions': ['1685085314', '1685085349', '1685105067']}
    start_spider_={'node_name': 'Leo-LPT', 'status': 'ok', 'jobid': '527eb7c7fbd111ed91888cc681ed1a0d'}
    jobs={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '527eb7c7fbd111ed91888cc681ed1a0d'}], 'running': [], 'finished': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '5197dfd3fbc411eda66d8cc681ed1a0d', 'start_time': '2023-05-26 20:53:33.227064', 'end_time': '2023-05-26 20:53:41.825362', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.jl'}, {'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '85a1742bfbc411ed94908cc681ed1a0d', 'start_time': '2023-05-26 20:55:03.226823', 'end_time': '2023-05-26 20:55:11.954153', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/85a1742bfbc411ed94908cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/85a1742bfbc411ed94908cc681ed1a0d.jl'}]}
    jobs={'node_name': 'Leo-LPT', 'status': 'ok', 'pending': [], 'running': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '527eb7c7fbd111ed91888cc681ed1a0d', 'pid': 36708, 'start_time': '2023-05-26 22:26:38.227264'}], 'finished': [{'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '5197dfd3fbc411eda66d8cc681ed1a0d', 'start_time': '2023-05-26 20:53:33.227064', 'end_time': '2023-05-26 20:53:41.825362', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/5197dfd3fbc411eda66d8cc681ed1a0d.jl'}, {'project': 'phone_crawler', 'spider': 'PhoneBrandSpider', 'id': '85a1742bfbc411ed94908cc681ed1a0d', 'start_time': '2023-05-26 20:55:03.226823', 'end_time': '2023-05-26 20:55:11.954153', 'log_url': '/logs/phone_crawler/PhoneBrandSpider/85a1742bfbc411ed94908cc681ed1a0d.log', 'items_url': '/items/phone_crawler/PhoneBrandSpider/85a1742bfbc411ed94908cc681ed1a0d.jl'}]}
    cancel={'node_name': 'Leo-LPT', 'status': 'ok', 'prevstate': None}
"""
