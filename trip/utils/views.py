# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/15
"""
from functools import wraps

from utils.response import UnauthorizedJsonResponse


def login_required(view_func):
    """登录校验：如果用户未登录，返回401"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return UnauthorizedJsonResponse()
        return view_func(request, *args, **kwargs)

    return _wrapped_view
