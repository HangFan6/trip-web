# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/15 
"""
from django.urls import path

from order import views

urlpatterns = [
    # 订单提交接口
    path("ticket/submit/", views.TicketOrderSubmitView.as_view(), name='ticket_submit'),
    # 订单详情（支付、取消、删除订单）
    path("order/detail/<int:sn>/", views.OrderDetailView.as_view(), name='order_detail'),
    # 订单列表
    path("order/list/", views.OrderListView.as_view(), name='order_list'),
]
