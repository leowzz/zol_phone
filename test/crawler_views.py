from unittest import TestCase
from django.test import RequestFactory
from django.core.cache import cache

from django.http import HttpResponse, JsonResponse
from apps.crawler.views import SpiderView, JobsView, StartSpider


class SpiderViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_spider_view(self):
        request = self.factory.get('/spiders')
        response = SpiderView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        # Add more assertions to verify the response content and context if necessary


class JobsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Set up cache data for testing
        cache.set('projects', {'projects': ['project1', 'project2']})

    def tearDown(self):
        # Clear cache data after each test
        cache.clear()

    def test_get_jobs_view(self):
        request = self.factory.get('/jobs')
        response = JobsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        # Add more assertions to verify the response content and context if necessary


