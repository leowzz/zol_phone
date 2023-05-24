#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/22
from django.urls import path

from apps.crawler.views import SpiderView

urlpatterns = [
    # path('', CenterView.as_view()),
    path('spiders/', SpiderView.as_view()),
]
