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


class JobsView(View):
    @logger.catch
    @xframe_options_exempt
    def get(self, request):
        # 获取爬虫运行状态
        job_status = get_status()
        logger.debug(f"{job_status=}")
        # 如果scrapyd服务没有启动，返回错误页面
        if job_status.get('status') != 'ok':
            return render(request, '50x.html', context={
                'code': 500,
                'msg' : job_status.get('status')
            }, status=500)

        return render(request, 'jobs_list.html', context={
            'job_status': job_status,
            'title'     : '爬虫运行状态',
        })


def crawl(spider, **kwargs):
    runner = CrawlerRunner(get_project_settings())
    dfd = runner.crawl(spider, **kwargs)
    dfd.addBoth(lambda _: reactor.stop())
    reactor.run()


def start_spider(request, spider_name):
    spider = globals().get(spider_name)
    crawl(spider)
    return JsonResponse({'msg': 'ok'})


def scrape(request):
    process = CrawlerProcess(get_project_settings())
    process.crawl(PhoneBrandSpider)
    process.start()
    return jsonify({'msg': 'ok'})


if __name__ == '__main__':
    get_status()
