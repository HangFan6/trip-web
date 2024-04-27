# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/8 
"""
from django.db import models


class CommonModel(models.Model):
    """模型公共类"""
    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True  # 不需要创建新的数据表
