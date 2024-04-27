import json

from django import http
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.base import View

from accounts import serializers
from accounts.forms import LoginForm, RegisterForm
from utils.response import BadRequestJsonResponse, MethodNotAllowedJsonResponse, UnauthorizedJsonResponse, \
    ServerErrorJsonResponse


def user_login(request):
    """ 用户登录 """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            form.do_login(request)
            print('表单验证通过')
            return redirect('/accounts/user/info/')
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {
        'form': form
    })


# -----使用装饰器，要求用户必须登录----------
# 方法1
# @login_required(login_url='/accounts/user/login/')
# 方法2：在setting.py中配置跳转的URL
@login_required()
def user_info(request):
    """ 用户信息 """
    print(request.user)
    return render(request, 'user_info.html')


def user_logout(request):
    """用户退出登录"""
    logout(request)
    return redirect('/accounts/user/info/')


def user_api_login(request):
    """用户登录接口-POST"""
    # 获取输入的内容
    if request.method == 'POST':
        # 表单验证
        form = LoginForm(request.POST)
        # 如果验证通过，执行登录
        if form.is_valid():
            user = form.do_login(request)
            profile = user.profile
            # 返回内容：用户信息
            data = {
                'user': serializers.UserSerializer(user).to_dict(),
                'profile': serializers.UserProfile(profile).to_dict()
            }
            return http.JsonResponse(data)
        else:
            # 如果未通过验证：返回表单验证的错误信息
            # loads(form.errors.as_json())将json字符串转换成python对象
            err = json.loads(form.errors.as_json())
            # return http.JsonResponse(err)
            return BadRequestJsonResponse(err)
    else:
        # 请求不被允许
        return MethodNotAllowedJsonResponse()


def user_api_logout(request):
    """用户退出接口"""
    logout(request)
    return http.HttpResponse(status=201)


class UserDetailView(View):
    """用户详细信息接口"""

    def get(self, request):
        # 获取用户信息
        user = request.user
        # 判断用户类型：游客、注册用户
        if not user.is_authenticated:
            # 返回4010状态码
            return UnauthorizedJsonResponse()
        else:
            # 返回详细信息
            profile = user.profile
            data = {
                'user': serializers.UserSerializer(user).to_dict(),
                'profile': serializers.UserProfile(profile).to_dict()
            }
            return http.JsonResponse(data)


def user_api_register(request):
    """用户注册"""
    # 表单验证用户的输入信息（用户名、昵称、验证码）
    # 创建用户基础信息表、用户信息信息表
    # 执行登录
    # 保存登录日志
    pass


class UserRegisterView(FormView):
    """用户注册接口"""
    form_class = RegisterForm
    http_method_names = ['post']

    def form_valid(self, form):
        """表单已经通过验证"""
        result = form.do_register(request=self.request)
        if result is not None:
            user, profile = result
            data = {
                'user': serializers.UserSerializer(user).to_dict(),
                'profile': serializers.UserProfile(profile).to_dict()
            }
            return http.JsonResponse(data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """表单未通过验证"""
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)
