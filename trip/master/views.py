from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils.timezone import now

from accounts.models import User, Profile
from order.choices import OrderStatus
from order.models import Order
from sight.models import Sight, Comment


def test(request):
    """echarts的使用"""
    return render(request, 'master/test.html')


def get_data_count(start=None, end=None):
    """
    实时数据统计
    :param start:开始时间
    :param end:结束时间
    :return:
    """
    query = Q()
    if start:
        query = query & Q(created_at__gte=start)
    if end:
        query = query & Q(created_at__lte=end)
    order_list = Order.objects.filter(status=OrderStatus.PAID).filter(query)
    user_list = Profile.objects.select_related('user').filter(user__is_active=True).filter(query)
    now_stats = {
        # 销售额
        'order_amount': order_list.aggregate(amount=Sum('buy_amount'))['amount'],
        # 订单数量
        'order_count': order_list.count(),
        # 新增用户数
        'order_add_count': user_list.count(),
        # 下单用户数
        'order_user_count': order_list.values('user').distinct().count()
    }
    return now_stats


def get_latest_order_stats(days=7):
    """
    最近N日的订单统计
    :param days: 天数
    :return:
    """
    date_array, amount_array, count_array = [], [], []
    now_time = now()
    for x in range(days, 0, -1):
        # 日期
        calc_time = now_time + timedelta(hours=-x * 24)
        # 注意！！！：在HTML中传参时，要防止转义（{{ latest_stats.date|safe }}）
        date_array.append('{}号'.format(calc_time.day))
        queryset = Order.objects.filter(status=OrderStatus.PAID, created_at__date=calc_time.date())
        result = queryset.aggregate(amount=Sum('buy_amount'), count=Sum('buy_count'))
        # 订单金额
        amount_array.append(result['amount'] or 0)
        # 订单数量
        count_array.append(result['count'] or 0)
    latest_stats = {
        'date': date_array,
        'amount': amount_array,
        'count': count_array,
    }
    return latest_stats


# 具有管理权限，才可查看报表
@login_required(login_url='/admin/login/')
def index(request):
    """订单统计报表"""
    # 1、数据统计
    total_stats = {
        'sight_count': Sight.objects.filter(is_valid=True).count(),
        'comment_count': Comment.objects.filter(is_valid=True).count(),
        'user_count': User.objects.filter(is_active=True).count(),
        'order_count': Order.objects.filter(status=OrderStatus.PAID).count(),
    }
    # 2、今日实时数据
    now_time = now()
    now_stats = get_data_count(start=datetime(now_time.year, now_time.month, now_time.day))
    # 3、昨天数据
    yesterday = now_time + timedelta(hours=-24)
    yesterday_stats = get_data_count(
        start=datetime(yesterday.year, yesterday.month, yesterday.day),
        end=datetime(now_time.year, now_time.month, now_time.day)
    )
    # 4、数据走势
    latest_stats = get_latest_order_stats()
    return render(request, 'master/index.html', {
        'total_stats': total_stats,
        'now_stats': now_stats,
        'yesterday_stats': yesterday_stats,
        'latest_stats': latest_stats
    })
