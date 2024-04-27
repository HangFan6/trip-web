import json

from django import http
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from system.forms import SendSmsCodeForm
from system.models import Slider
from utils.response import ServerErrorJsonResponse, BadRequestJsonResponse


def slider_list(request):
    """轮播图接口"""
    data = {
        'meta': {},
        'objects': []
    }
    queryset = Slider.objects.filter(is_valid=True)
    for item in queryset:
        data['objects'].append({
            'id': item.id,
            'img_url': item.img.url,
            'target_url': item.target_url,
            'name': item.name
        })
    # return HttpResponse(data)
    return http.JsonResponse(data)


def cache_set(request):
    """写缓存"""
    cache.set('username', 'lisi')
    # 超时5秒后自动删除
    cache.set('password', 'password', timeout=5)
    return HttpResponse('ok')


def cache_get(request):
    """读取缓存"""
    value = cache.get('username')
    return HttpResponse(value)


def send_sms(request):
    """发送验证码"""
    pass
    # 拿到手机号，判断是否为真实手机号
    # 生成验证码，并存储
    # TODO 调用短信发送接口（收费）
    # 告诉用户验证码是否发送成功（学习：将验证码直接告诉用户）


class SmsCodeView(FormView):
    form_class = SendSmsCodeForm

    def form_valid(self, form):
        """表单已经通过验证"""
        data = form.send_sms_code()
        if data is not None:
            return http.JsonResponse(data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """表单未通过验证"""
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)
