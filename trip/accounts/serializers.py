# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/13 
"""
from utils.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    """用户的基础信息"""

    def to_dict(self):
        user = self.obj
        return {
            'username': user.username,
            'nickname': user.nickname,
            'avatar': user.avatar_url
        }


class UserProfile(BaseSerializer):
    """用户的详细信息"""

    def to_dict(self):
        profile = self.obj
        return {
            'real_name': profile.real_name,
            'sex': profile.sex,  # 返回值为数值
            'sex_display': profile.get_sex_display()  # 返回值为数值对应的中文信息
        }
