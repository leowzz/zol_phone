#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/22
from django.urls import path

from apps.crawler.views import SpiderView, get_status, JobsView, StartSpider

urlpatterns = [
    # path('', CenterView.as_view()),
    path('spiders/', SpiderView.as_view()),
    path('spiders/run', StartSpider.as_view()),
    path('spiders/jobs/', JobsView.as_view()),
    # path('spiders/progress', get_status),
]
