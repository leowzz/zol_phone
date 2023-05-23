from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apps.crawler.spiders.phone_brand_spider import ZolSpider
# Create your views here.


def scrape(request):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ZolSpider)
    process.start()
    return jsonify({'msg': 'ok'})


if __name__ == '__main__':
    scrape()