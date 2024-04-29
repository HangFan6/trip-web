# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/13 
"""
import random
import re
from django import forms
from django.core.cache import cache

from utils import constants


class SendSmsCodeForm(forms.Form):
    """发送验证码表单"""
    phone_num = forms.CharField(label='手机号码', required=True, error_messages={
        'required': '请输入手机号码'
    })

    def clean_phone_num(self):
        """验证是否为手机号码"""
        phone_num = self.cleaned_data['phone_num']
        pattern = r'^1[0-9]{10}$'
        if not re.search(pattern, phone_num):
            raise forms.ValidationError('手机号%s输入不正确',
                                        code='invalid_phone',
                                        params=(phone_num,))
        return phone_num

    def send_sms_code(self):
        """生成验证码并发送短信"""
        sms_code = random.randint(100000, 999999)
        phone_num = self.cleaned_data.get('phone_num', None)
        try:
            # TODO 调用发送短信验证码的接口
            # Redis中的key值
            # key = 'sms_code_{}'.format(phone_num)
            key = '{}{}'.format(constants.REGISTER_SMS_CODE_KEY, phone_num)
            # 将验证码存入Redis
            timeout = 5 * 60
            cache.set(key, sms_code, timeout=timeout)
            return {
                'phone_num': phone_num,
                'sms_code': sms_code,
                'time_out': timeout
            }
        except Exception as e:
            print(e)
            return None