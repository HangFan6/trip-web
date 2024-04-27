# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/8 
"""
from django.urls import path
from accounts import views


urlpatterns = [
    # 用户登录表单
    path("user/login/", views.user_login, name='user_login'),
    # 用户详细信息
    path("user/info/", views.user_info, name='user_info'),
    # 用户退出登录
    path("user/logout/", views.user_logout, name='user_logout'),
    # 登录与退出接口
    path("user/api/login/", views.user_api_login, name='user_api_login'),
    path("user/api/logout/", views.user_api_logout, name='user_api_logout'),
    # 用户详细信息接口（使用面向对象的方式实现函数）
    path("user/api/info/", views.UserDetailView.as_view(), name='user_api_info'),
    # 用户注册表单
    path("user/api/register/", views.UserRegisterView.as_view(), name='user_api_register'),
]
