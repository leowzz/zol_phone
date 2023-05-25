from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apps.crawler.spiders.phone_brand_spider import PhoneBrandSpider
from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.

from django.views.decorators.clickjacking import xframe_options_exempt


class SpiderView(View):
    # 现代浏览器采用X - Frame - Options
    # HTTP标头，该标头指示是否允许在框架或iframe中加载资源。如果响应包含标头值为的标头，SAMEORIGIN则浏览器将仅在请求源自同一站点的情况下将资源加载到框架中。如果将标头设置为，DENY则无论哪个站点发出请求，浏览器都将阻止资源加载到框架中。
    @xframe_options_exempt
    def get(self, request):
        return render(request, 'spiders_list.html', context={'title': '爬虫列表', 'content': 'PhoneBrandSpider'})


def scrape(request):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZolSpider)
    process.start()
    return jsonify({'msg': 'ok'})


if __name__ == '__main__':
    scrape()
