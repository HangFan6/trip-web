# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/9 
"""
from utils.serializers import BaseSerializer


class BaseImageSerializer(BaseSerializer):
    """序列化基础图片：其他列表需要引用到时再进行使用"""

    def to_dict(self):
        image = self.obj
        return {
            'img': image.img.url,
            'summary': image.summary
        }
