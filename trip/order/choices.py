# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/14 
"""
from django.db import models


class OrderStatus(models.IntegerChoices):
    """订单状态"""
    SUBMIT = 11, '待支付'
    PAID = 12, '以支付'
    CANCELED = 13, '已取消'


class OrderTypes(models.IntegerChoices):
    """订单类型"""
    SIGHT_TICKET = 10, '门票'
    HOTEL = 11, '酒店'
