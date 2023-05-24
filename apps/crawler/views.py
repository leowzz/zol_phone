from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apps.crawler.spiders.phone_brand_spider import PhoneBrandSpider
from django.shortcuts import render, HttpResponse
from django.views import View


# Create your views here.

class SpiderView(View):
    def get(self, request):
        return render(request, 'spiders_list.html', context={'title': '爬虫列表', 'content': 'PhoneBrandSpider'})


def scrape(request):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZolSpider)
    process.start()
    return jsonify({'msg': 'ok'})


if __name__ == '__main__':
    scrape()
