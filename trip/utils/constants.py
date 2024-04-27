# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/13 
"""
# 用户注册时，发送验证码的Redis key
REGISTER_SMS_CODE_KEY = 'reg_sms_'
# 缓存首页的精选/热门景点Redis key
INDEX_SIGHT_TOP_KEY = 'index_top'
INDEX_SIGHT_HOT_KEY = 'index_hot'
# 缓存时间
INDEX_SIGHT_TIMEOUT = 2*60*60
