#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/26

import os
import sys

from zol_phone.settings import BASE_DIR, SCRAPYD_PROJECT_NAME

scrapyd_proj_path = os.path.join(BASE_DIR, SCRAPYD_PROJECT_NAME)

os.system(rf"scrapyd -d {scrapyd_proj_path}")
