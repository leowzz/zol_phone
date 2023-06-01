#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/6/1
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from django.core.cache import cache
from apps.visual.views import BrandView, Echarts
from apps.crawler.models import Phone_brand, Phone_sku, Phone_spu


class BrandViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_brand_view(self):
        # Create and save some Phone_brand objects in the database
        brand1 = Phone_brand.objects.create(name='Brand1', market_share=10, phone_num=100, feedback=4.5)
        brand2 = Phone_brand.objects.create(name='Brand2', market_share=15, phone_num=150, feedback=4.3)

        request = self.factory.get('/brand')
        response = BrandView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        # Add more assertions to verify the response content and data if necessary

        # Clean up: Delete the created Phone_brand objects
        brand1.delete()
        brand2.delete()


class EchartsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_echarts_view(self):
        # Create and save some Phone_sku and Phone_spu objects in the database
        phone1 = Phone_sku.objects.create(name='Phone1', comments_num=100, price=500, score=4.5)
        phone2 = Phone_sku.objects.create(name='Phone2', comments_num=150, price=600, score=4.3)
        spu1 = Phone_spu.objects.create(name='Phone1', mall_price=550)
        spu2 = Phone_spu.objects.create(name='Phone2', mall_price=650)

        request = self.factory.get('/echarts')
        response = Echarts.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        # Add more assertions to verify the response content and data if necessary

        # Clean up: Delete the created Phone_sku and Phone_spu objects
        phone1.delete()
        phone2.delete()
        spu1.delete()
        spu2.delete()
