# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/20 
"""
from django.contrib import messages


# def set_invalid(self, request, queryset):
def set_invalid(modeladmin, request, queryset):
    """批量禁用"""
    queryset.update(is_valid=False)
    # 消息闪现
    messages.success(request, '禁用成功')


def set_valid(modeladmin, request, queryset):
    """批量启用"""
    queryset.update(is_valid=True)
    messages.success(request, '启用成功')


set_invalid.short_description = '禁用所选对象'
set_valid.short_description = '启用所选对象'
