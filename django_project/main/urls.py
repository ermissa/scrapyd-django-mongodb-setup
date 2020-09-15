from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView, RedirectView
from . import views


urlpatterns = [
    path('crawl', views.crawl, name="crawl"),
]
