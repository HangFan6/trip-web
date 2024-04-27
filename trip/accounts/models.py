from django.db import models
from utils.models import CommonModel
from django.contrib.auth.models import AbstractUser


# class User(CommonModel):
#     """用户模型"""
#     username = models.CharField('用户名', max_length=32)
#     password = models.CharField('密码', max_length=256)
#     avatar = models.ImageField('用户头像', upload_to='avatar/%Y%m%d', null=True, blank=True)
#     nickname = models.CharField('昵称', max_length=32, unique=True)
#
#     class Meta:
#         db_table = 'account_user'


# 继承自django中的AbstractUser抽象模型
class User(AbstractUser):
    """用户模型"""
    # 添加字段
    avatar = models.ImageField('用户头像', upload_to='avatar/%Y%m%d', null=True, blank=True)
    nickname = models.CharField('昵称', max_length=32, unique=True)

    class Meta:
        db_table = 'account_user'
        # Django后台中文显示时，设置的中文名称
        verbose_name = '用户信息'
        # 列表有多项，在英文中有复数形式，故显示（用户信息s），verbose_name_plural去除复数s
        verbose_name_plural = '用户信息'

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else ''

    def add_login_record(self, **kwargs):
        """保存登录历史"""
        self.login_records.create(**kwargs)


class Profile(models.Model):
    """用户详细信息"""
    SEX_CHOICES = (
        (1, '男'),
        (0, '女'),
    )
    username = models.CharField('用户姓名', max_length=64, unique=True, editable=False)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, editable=False)
    # 真实姓名
    real_name = models.CharField('真实姓名', max_length=32)
    # 电子邮箱
    email = models.CharField('电子邮箱', max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField('邮箱是否已经验证', default=False)
    # 手机号码
    phone_no = models.CharField('手机号码', max_length=20, null=True, blank=True)
    is_phone_valid = models.BooleanField('手机号是否已验证', default=False)
    # 性别
    sex = models.SmallIntegerField('性别', default=1, choices=SEX_CHOICES)
    # 年龄
    age = models.SmallIntegerField('年龄', default=0)
    source = models.CharField('登录来源', max_length=16, null=True)
    version = models.CharField('登录的版本', max_length=16, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        # Django后台中文显示时，设置的中文名称
        verbose_name = '用户详细信息'
        # 列表有多项，在英文中有复数形式，故显示（用户详细信息s），verbose_name_plural去除复数s
        verbose_name_plural = '用户详细信息'

    def __str__(self):
        """重写Admin用户修改后，返回的提示"""
        return self.username


class LoginRecord(models.Model):
    """用户登录日志"""
    user = models.ForeignKey(User, related_name='login_records', on_delete=models.CASCADE)
    username = models.CharField('登录的账号', max_length=64)
    ip = models.CharField('IP', max_length=32)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登录来源', max_length=16, null=True)
    version = models.CharField('登录版本', max_length=16, null=True)
    created_at = models.DateTimeField('登录时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_login_record'
