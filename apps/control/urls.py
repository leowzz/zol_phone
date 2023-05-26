#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/22
from django.urls import path

from apps.control.views import IndexView, home_page

urlpatterns = [
    path('', IndexView.as_view()),
    path('index/', IndexView.as_view()),
    path('home_page/', home_page),
]
