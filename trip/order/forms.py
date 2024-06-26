# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/15 
"""
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F

from order.models import Order, OrderItem
from sight.models import Ticket
from utils import tools


class SubmitTicketOrderForm(forms.ModelForm):
    """门票订单提交表单"""
    ticket_id = forms.IntegerField(label='门票ID', required=True)
    play_date = forms.DateField(label='出行时间', required=True)

    class Meta:
        model = Order
        fields = ('to_user', 'to_phone', 'buy_count',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticket = None

    # 门票ID验证
    def clean_ticket_id(self):
        ticket_id = self.cleaned_data['ticket_id']
        ticket = Ticket.objects.select_related('sight').filter(is_valid=True, pk=ticket_id).first()
        if ticket is None:
            raise forms.ValidationError('门票信息不存在')
        else:
            if ticket.remain_stock <= 0:
                raise forms.ValidationError('当日门票已售完')
        self.ticket = ticket
        return ticket_id

    # 重写order数据表保存方法
    @transaction.atomic
    def save(self, user, commit=False):
        obj = super().save(commit=commit)
        obj.user = user
        # 生成订单号
        obj.sn = tools.gen_trans_id()
        # 计算价格
        buy_count = self.cleaned_data['buy_count']
        buy_amount = self.ticket.sale_price * buy_count
        obj.buy_amount = buy_amount
        obj.save()
        # 扣减库存
        self.ticket.remain_stock = F('remain_stock') - buy_count
        self.ticket.save()
        # 关联订单明细，保存快照
        ctype = ContentType.objects.get_for_model(Ticket)
        OrderItem.objects.create(
            user=user,
            order=obj,
            flash_name=self.ticket.name,
            flash_img=self.ticket.sight.main_img,
            flash_price=self.ticket.sale_price,
            flash_origin_price=self.ticket.price,
            flash_discount=self.ticket.discount,
            count=buy_count,
            amount=buy_amount,
            content_type=ctype,
            object_id=self.ticket.id,
            remark='出行时间：{}'.format(self.cleaned_data['play_date'])
        )
        return obj
