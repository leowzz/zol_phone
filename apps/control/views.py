from django.shortcuts import render, redirect
from django.views import View


# Create your views here.

class IndexView(View):
    def get(self, request):
        return redirect('/static/index.html')
