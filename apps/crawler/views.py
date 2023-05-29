from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.http import JsonResponse
# Create your views here.
from collections import defaultdict
from django.views.decorators.clickjacking import xframe_options_exempt
from loguru import logger
from apps.crawler.utils import *
from django.core.cache import cache
from utils.cacher import cache_handler
from utils.decorators import resp_500


class SpiderView(View):
    # 现代浏览器采用X - Frame - Options
    # HTTP标头，该标头指示是否允许在框架或iframe中加载资源。如果响应包含标头值为的标头，SAMEORIGIN则浏览器将仅在请求源自同一站点的情况下将资源加载到框架中。如果将标头设置为，DENY则无论哪个站点发出请求，浏览器都将阻止资源加载到框架中。

    @xframe_options_exempt
    def get(self, request):
        # 获取所有项目名称
        # 缓存处理
        cache_projects = cache_handler('projects', get_project_list, 20 * 60)
        logger.debug(f"{cache_projects=}")
        # 如果scrapyd服务没有启动，返回错误页面
        if cache_projects.get('status') != 'ok':
            return render(request, '50x.html', context={
                'code': 500,
                'msg' : cache_projects.get('scrapyd error')
            }, status=500)
        project_names = cache_projects["projects"]
        # 获取项目名称, 过滤掉 default
        projects = {project: {"spiders": []} for project in project_names if project != 'default'}
        logger.debug(f"{projects=}")

        # 获取每个项目下的爬虫名称
        for project in projects:
            spider_list = cache_handler(
                f'spiders_{project}',
                get_spider_list,
                20,
                project)
            logger.debug(f"{spider_list=}")
            if spider_list.get('status') == 'ok':
                projects[project]['spiders'].extend([_ for _ in spider_list.get('spiders') if _ != '\x1b[0m'])
        logger.debug(f"{projects=}")

        return render(request, 'spiders_list.html', context={
            'projects': projects,
            'title'   : '爬虫信息',
        })


# 所有状态信息 与 中文名称的映射
_status_names = {
    'pending' : '等待中',
    'running' : '运行中',
    'finished': '已完成',
}


class JobsView(View):
    @xframe_options_exempt
    def get(self, request):
        # 获取所有项目名称
        cache_projects = cache_handler('projects', get_project_list, 20 * 60)
        logger.debug(f"{cache_projects=}")
        # 以状态为键，jobs为值，构建字典
        jobs_status_list = defaultdict(list)
        project_names = [_ for _ in cache_projects.get('projects') if _ != 'default']
        for project in project_names:
            # 获取爬虫运行状态
            _jobs = get_jobs(project)
            logger.debug(f"{_jobs=}")
            # 如果scrapyd服务没有启动，返回错误页面
            if _jobs.get('status') != 'ok':
                return render(request, '50x.html', context={
                    'code': 500,
                    'msg' : _jobs.get('msg')
                }, status=500)
            for status_name in _status_names:
                jobs_status_list[status_name].extend(_jobs.get(status_name))

        logger.debug(f"{jobs_status_list=}")
        jobs_status_cnt = {}
        for status_name in _status_names:
            jobs_status_cnt[_status_names[status_name]] = len(jobs_status_list.get(status_name))
        logger.debug(f"{jobs_status_cnt=}")
        # 获取所有jobs信息
        all_jobs = []
        for status_name in _status_names:
            for job in jobs_status_list.get(status_name):
                job['status'] = _status_names[status_name]
                all_jobs.append(job)

        return render(request, 'jobs_list.html', context={
            'job_status': jobs_status_cnt,
            'jobs'      : all_jobs,
            'title'     : '爬虫运行状态',
        })


import json


class StartSpider(View):
    def post(self, request):
        project = request.POST.get('project')
        spider = request.POST.get('spider')
        # 启动爬虫
        logger.info(f"启动爬虫: {project} {spider}")
        res = start_spider(project, spider)
        logger.debug(f"{res=}")
        return JsonResponse(res)
