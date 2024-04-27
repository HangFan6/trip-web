# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/20 
"""
from django.urls import path

from master import views

urlpatterns = [
    # echarts的使用
    path("test/", views.test, name="test"),
    # 订单统计报表
    path("", views.index, name="index"),
]