#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/27
"""
部署爬虫项目到 scrapyd
"""

import os
from zol_phone.settings import BASE_DIR, SCRAPYD_PROJECT_NAME

os.chdir(os.path.join(BASE_DIR, SCRAPYD_PROJECT_NAME))

os.system(f"scrapyd-deploy local -p {SCRAPYD_PROJECT_NAME}")
