from django.shortcuts import render
from apps.crawler.models import Phone_brand
from django.views import View
from loguru import logger
from django.http import JsonResponse


# Create your views here.

class BrandView(View):
    @logger.catch
    def get(self, request):
        # 获取所有品牌
        brands = Phone_brand.objects.all()
        return render(request, 'brand.html', context={
            'brands': brands,
        })
