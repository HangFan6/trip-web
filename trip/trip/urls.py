"""
URL configuration for trip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    # 系统模块
    path("system/", include('system.urls')),
    # 景点模块
    path("sight/", include('sight.urls')),
    # 用户账户模块
    path("accounts/", include('accounts.urls')),
    # 订单模块
    path("order/", include('order.urls')),
    # 富文本相关的配置
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # 后台管理统计报表
    path('master/', include('master.urls')),
]
