# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/4 
"""
from django.urls import path
from system import views

urlpatterns = [
    # 轮播图
    path("slider/list/", views.slider_list, name="slider_list"),
    # Redis缓存（验证码）
    path("cache/set/", views.cache_set, name="cache_set"),
    path("cache/get/", views.cache_get, name="cache_get"),
    # 发送验证码
    path("send/sms/", views.SmsCodeView.as_view(), name="send_sms"),
]
