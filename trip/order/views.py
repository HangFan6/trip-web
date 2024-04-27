import json

from django import http
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView
from django.views.generic.detail import BaseDetailView

from order import serializers
from order.choices import OrderStatus
from order.forms import SubmitTicketOrderForm
from order.models import Order
from utils.response import BadRequestJsonResponse, NotFoundJsonResponse
from utils.views import login_required


def ticket_submit(request):
    """订单"""
    # 0、验证用户是否已经登录
    # 1、获取post数据
    # 2、数据的验证（手机号、门票ID、库存）
    # 3、关联用户、生成订单号、计算购买总价、生成订单（ORDER）
    # 4、返回内容：订单ID
    pass


# 使用该接口时，需要用户是登录状态；dispatch分发时（检测用户是否登录）
@method_decorator(login_required, name='dispatch')
class TicketOrderSubmitView(FormView):
    """门票订单提交接口"""
    form_class = SubmitTicketOrderForm
    http_method_names = ['post']

    def form_invalid(self, form):
        """表单未通过验证"""
        err = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err)

    def form_valid(self, form):
        """表单通过验证"""
        obj = form.save(user=self.request.user)
        return http.JsonResponse({
            'sn': obj.sn
        }, status=201)


# 使用该接口时，需要用户是登录状态
# dispatch分发时（检测用户是否登录），面向对象，根据不同请求方式，分配到不同的方法上进行处理
@method_decorator(login_required, name='dispatch')
class OrderDetailView(BaseDetailView):
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user, is_valid=True)

    def get(self, *args, **kwargs):
        """GET 订单详情"""
        order_obj = self.get_object()
        data = serializers.OrderDetailSerializer(order_obj).to_dict()
        return http.JsonResponse(data)

    # 确保事务的一致性
    @transaction.atomic
    def post(self, *args, **kwargs):
        """POST 订单支付"""
        # 0、TODO 选择支付方式：支付宝、微信（暂时省略）
        # 1、获取订单对象
        order_obj = self.get_object()
        # 2、数据验证
        if order_obj.status == OrderStatus.SUBMIT:
            # 3、TODO 调用真实的支付方式（暂时省略）
            # 4、改变订单状态
            order_obj.status = OrderStatus.PAID
            order_obj.save()
            order_obj.order_items.update(status=OrderStatus.PAID)
            # 支付成功，返回201
            return http.HttpResponse('', status=201)
        # 已经是被支付状态，返回200
        return http.HttpResponse('', status=200)
        # return http.JsonResponse({'result': 'post'})

    def delete(self, *args, **kwargs):
        """DELETE 订单删除"""
        # 1、获取订单对象
        order_obj = self.get_object()
        # 2、数据验证，判断状态（已支付、已取消）
        if order_obj.status == OrderStatus.CANCELED or order_obj.status == OrderStatus.PAID:
            # 3、是否已经删除过
            if order_obj.is_valid:
                # 未删除，进行逻辑删除
                order_obj.is_valid = False
                order_obj.save()
                return http.HttpResponse('', status=201)
            else:
                # 此处不用写，因为get_obj已经触发404
                pass
        # 订单类型不能被删除
        return http.HttpResponse('', status=200)
        # return http.JsonResponse({'result': 'delete'})

    @transaction.atomic
    def put(self, *args, **kwargs):
        """PUT 订单取消"""
        # 1、获取订单对象
        order_obj = self.get_object()
        # 2、数据验证，判断状态
        if order_obj.status == OrderStatus.SUBMIT:
            # 3、改变状态
            order_obj.status = OrderStatus.CANCELED
            order_obj.save()
            items = order_obj.order_items.filter(status=OrderStatus.SUBMIT)
            # 4、加回已减扣的库存（注意：购买数量可能变化）
            for item in items:
                obj = item.content_object
                obj.remain_stock = F('remain_stock') + item.count
                obj.save()
            items.update(status=OrderStatus.CANCELED)
            # 取消成功，返回201
            return http.HttpResponse('', status=201)
            # 已经是被取消状态，返回200
        return http.HttpResponse('', status=200)
        # return http.JsonResponse({'result': 'put'})


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    """我的订单列表"""
    # 每页10条数据
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        query = Q(is_valid=True, user=user)
        # 按照订单状态查询
        status = self.request.GET.get('status', None)
        if status and status != '0':
            query = query & Q(status=status)
        return Order.objects.filter(query)

    def render_to_response(self, context, **response_kwargs):
        """重写响应返回"""
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.OrderListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()

    def get_paginate_by(self, queryset):
        """重写前端传入的列表分页大小"""
        # 通过接口参数limit来控制分页的大小
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by
