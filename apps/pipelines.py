#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/5/22
from django.db import IntegrityError
from scrapy.exceptions import DropItem
from scrapy_app.models import Product


class ScrapyAppPipeline:
    def process_item(self, item, spider):
        try:
            product = Product(**item)
            product.save()
        except IntegrityError:
            raise DropItem("Duplicate item found: %s" % item['name'])
        return item
