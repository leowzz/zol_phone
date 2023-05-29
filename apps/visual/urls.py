#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/29
from django.urls import path

from apps.visual.views import BrandView, Echarts

urlpatterns = [
    # path('', CenterView.as_view()),
    path('brands/visual/', BrandView.as_view()),
    path('phones/echarts/', Echarts.as_view()),
]
