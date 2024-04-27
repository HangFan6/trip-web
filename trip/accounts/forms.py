import re
from django import forms
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.db import transaction
from django.utils.timezone import now

from accounts.models import User, Profile
from utils import constants


class LoginForm(forms.Form):
    """ 登录表单 """
    username = forms.CharField(label='用户名',
                               max_length=100,
                               required=False,
                               help_text='使用帮助',
                               initial='admin')
    password = forms.CharField(label='密码', max_length=200, min_length=6,
                               widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 登录当前用户
        self.user = None

    def clean_username(self):
        """ 验证用户名 hook 钩子函数 """
        username = self.cleaned_data['username']
        pattern = r'^1[0-9]{10}$'
        if not re.search(pattern, username):
            raise forms.ValidationError('手机号%s输入不正确',
                                        code='invalid_phone',
                                        params=(username,))
        return username

    def clean(self):
        data = super().clean()
        print(data)
        # 如果单个字段有错误，直接返回，不执行后面的验证
        if self.errors:
            return
        # username = data['username']
        # password = data['password']
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            if not user.is_active:
                raise forms.ValidationError('该用户已经被禁用')
        self.user = user

        # if username and password:
        #     # 1、查询用户名和密码匹配的用户
        #     user_list = User.objects.filter(username=username)
        #     err_list = []
        #     if user_list.count() == 0:
        #         err_list.append(forms.ValidationError('用户名不存在'))
        #         # raise forms.ValidationError('用户名不存在')
        #     # 2、验证密码是否正确
        #     # 3、TODO 使用加密算法进行验证
        #     if not user_list.filter(password=password).exists():
        #         # raise forms.ValidationError('密码不正确')
        #         err_list.append(forms.ValidationError('密码不正确'))
        #     if err_list:
        #         raise forms.ValidationError(err_list)
        return data

    def do_login(self, request):
        """用户登录"""
        user = self.user
        # 调用登录
        login(request, user)
        # 修改最后登录时间
        user.last_login = now()
        user.save()
        # TODO 保存登录历史
        # 向表accounts_login_record中插入数据
        return user


class RegisterForm(forms.Form):
    """用户注册"""
    username = forms.CharField(label='手机号码', max_length=16, required=True, error_messages={
        'required': '请输入手机号码'
    })
    password = forms.CharField(label='密码', max_length=128, required=True, error_messages={
        'required': '请输入密码'
    })
    nickname = forms.CharField(label='昵称', max_length=16, required=True, error_messages={
        'required': '请输入昵称'
    })
    sms_code = forms.CharField(label='验证码', max_length=6, required=True, error_messages={
        'required': '请输入验证码'
    })

    def clean_username(self):
        """ 验证用户名 hook 钩子函数 """
        username = self.cleaned_data['username']
        pattern = r'^1[0-9]{10}$'
        if not re.search(pattern, username):
            raise forms.ValidationError('手机号%s输入不正确',
                                        code='invalid_phone',
                                        params=(username,))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('手机号码已被注册')
        return username

    def clean_nickname(self):
        """昵称验证"""
        nickname = self.cleaned_data['nickname']
        if User.objects.filter(username=nickname).exists():
            raise forms.ValidationError('该昵称已被使用')
        return nickname

    def clean(self):
        data = super().clean()
        if self.errors:
            return
        phone_num = self.cleaned_data.get('username', None)
        sms_code = self.cleaned_data.get('sms_code', None)
        # Redis中的验证码的key
        key = '{}{}'.format(constants.REGISTER_SMS_CODE_KEY, phone_num)
        code = cache.get(key)
        # code已失效
        if code is None:
            raise forms.ValidationError('验证码已失效')
        if str(code) != sms_code:
            raise forms.ValidationError('验证码输入不正确')
        return data

    # 使用装饰器，确保2个表同时创建成功或失败
    @transaction.atomic
    def do_register(self, request):
        """调用注册方法，执行注册"""
        data = self.cleaned_data
        version = request.headers.get('version', '')
        source = request.headers.get('source', '')
        try:
            # 创建基础信息表
            user = User.objects.create_user(
                username=data.get('username', None),
                password=data.get('password', None),
                nickname=data.get('nickname', None)
            )
            # 创建详细信息表
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                version=version,
                source=source
            )
            # 执行登录
            login(request, user)
            # 记录登录日志
            user.last_login = now()
            user.save()
            ip = request.META.get('REMOTE_ADDR', '')
            user.add_login_record(username=user.username, ip=ip, version=version, source=source)
            return user, profile
        except Exception as e:
            print(e)


class ProfileEditForm(forms.ModelForm):
    """后台管理：用户详细信息编辑"""

    class Meta:
        model = Profile
        fields = ('real_name', 'email', 'phone_no', 'sex', 'age')

    def clean_age(self):
        """验证用户的年龄"""
        age = self.cleaned_data['age']
        if int(age) >= 120 or int(age) <= 0:
            raise forms.ValidationError('年龄只能在0~120岁之间')
        return age

    def save(self, commit=False):
        obj = super().save(commit)
        # 保存数据时做其他的业务处理
        if not obj.source:
            obj.source = 'web'
            obj.save()
        return obj
