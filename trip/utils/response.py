# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/8 
"""
from django.http import JsonResponse


class NotFoundJsonResponse(JsonResponse):
    """400对应的JSON响应"""
    status_code = 404

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "404000",
            "error_message": "您访问的内容不存在或已删除。"
        }
        super().__init__(data, *args, **kwargs)


class BadRequestJsonResponse(JsonResponse):
    """表单验证请求没有通过，错误显示"""
    status_code = 400

    def __init__(self, err_list=[], *args, **kwargs):
        data = {
            "error_code": "400000",
            "error_msg": "参数格式不正确",
            "error_list": err_list
        }
        super().__init__(data, *args, **kwargs)


class MethodNotAllowedJsonResponse(JsonResponse):
    """请求方式不被允许"""
    status_code = 405

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "405000",
            "error_msg": "请求方式不被允许"
        }
        super().__init__(data, *args, **kwargs)


class UnauthorizedJsonResponse(JsonResponse):
    status_code = 401

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "401000",
            "error_msg": "请登录"
        }
        super().__init__(data, *args, **kwargs)


class ServerErrorJsonResponse(JsonResponse):
    status_code = 500

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "500000",
            "error_msg": "服务器正忙，请稍后重试"
        }
        super().__init__(data, *args, **kwargs)
