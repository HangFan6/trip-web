import json

from django import http
from django.core.cache import cache
from django.db.models import Q
# from django.shortcuts import render
from django.views.generic import ListView, DetailView

from sight import serializers
from sight.models import Sight, Comment, Ticket, Info
from utils import constants
from utils.response import NotFoundJsonResponse


class SightListView(ListView):
    """景点列表"""
    # 每页放条数据
    paginate_by = 5

    def get_queryset(self):
        """重写查询方法"""
        query = Q(is_valid=True)
        # 1、热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            query = query & Q(is_hot=True)
        # 2、精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            query = query & Q(is_top=True)
        # 3、景点名称搜索
        name = self.request.GET.get('name', None)
        if name:
            query = query & Q(name__icontains=name)
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        """从前端控制每一页的分页大小：有则替换，无则默认"""
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        # 从关系型数据库拿取数据
        # 查看context中的参数，也可以通过添加断点和调试模式查看
        # print("context is>>>", context)
        page_obj = context['page_obj']
        # 重构响应对象
        if page_obj is not None:
            data = serializers.SightListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()

        # data = {
        #     'meta': {
        #         # 通过调试获取page_obj中字对象
        #         'total_count': page_obj.paginator.count,
        #         'page_count': page_obj.paginator.num_pages,
        #         'current_count': page_obj.number,
        #     },
        #     'objects': []
        # }
        # for item in page_obj.object_list:
        #     data['objects'].append({
        #         'id': item.id,
        #         'name': item.name,
        #         'main_img': item.main_img.url,
        #         'score': item.score,
        #         'province': item.province,
        #         'city': item.city,
        #         'area': item.area,
        #         'min_price': item.min_price,
        #         # TODO 评论数量暂时无法获取
        #         'comment_count': 0
        #     })

        # print(data['objects'])
        # print(data['meta'])
        # print(http.JsonResponse(data))
        # return http.JsonResponse(data)


class SightListCacheView(ListView):
    """景点列表：缓存优化"""
    # 每页放条数据
    paginate_by = 20

    def get_queryset(self):
        """重写查询方法"""
        query = Q(is_valid=True)
        # 1、热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            query = query & Q(is_hot=True)
        # 2、精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            query = query & Q(is_top=True)
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        """从前端控制每一页的分页大小：有则替换，无则默认"""
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        # 1、从缓存拿取数据
        # 1、热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            try:
                data = cache.get(constants.INDEX_SIGHT_HOT_KEY)
                if data:
                    print(data)
                    return http.JsonResponse(json.loads(data))
            except Exception as e:
                print(e)
        # 2、精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            try:
                data = cache.get(constants.INDEX_SIGHT_TOP_KEY)
                if data:
                    print(data)
                    return http.JsonResponse(json.loads(data))
            except Exception as e:
                print(e)
        # 2、从关系型数据库拿取数据
        # 查看context中的参数，也可以通过添加断点和调试模式查看
        # print("context is>>>", context)
        page_obj = context['page_obj']
        # 重构响应对象
        if page_obj is not None:
            data = serializers.SightListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class SightDetailView(DetailView):
    """景点详细信息"""

    def get_queryset(self):
        # return Sight.objects.filter(is_valid=True)
        return Sight.objects.all()

    def render_to_response(self, context, **response_kwargs):
        # print("context is>>>", context)
        page_obj = context['object']
        if page_obj is not None:
            if not page_obj.is_valid:
                return NotFoundJsonResponse()
            data = serializers.SightDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class SightCommentListView(ListView):
    """景点下的评论列表"""
    # 分页查询，每页10条数据
    paginate_by = 10

    def get_queryset(self):
        # 根据景点ID查询景点
        sight_id = self.kwargs.get('pk', None)
        sight = Sight.objects.filter(pk=sight_id, is_valid=True).first()
        if sight:
            # return Comment.objects.filter(is_valid=True,sight=sight)
            return sight.comments.filter(is_valid=True)
        return Comment.objects.none()

    def render_to_response(self, context, **response_kwargs):
        """重写响应的返回"""
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.CommentListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightTicketListView(ListView):
    """景点下的门票列表"""
    paginate_by = 10

    def get_queryset(self):
        # 根据景点ID查询景点
        sight_id = self.kwargs.get('pk', None)
        return Ticket.objects.filter(is_valid=True, sight_id=sight_id)

    def render_to_response(self, context, **response_kwargs):
        """重写响应的返回"""
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.TicketListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightInfoDetailView(DetailView):
    """景点介绍"""
    # 默认情况下pk_url_kwarg是'pk'，其值为None表示不以模型主键作为查询参数
    # 只有为None时，下面的配置才会生效
    pk_url_kwarg = None
    # URL中参数的名称：sight/urls.py（sight/info/<int:pk>/）
    slug_url_kwarg = 'pk'
    # URL中pk对应到数据库中的字段名
    slug_field = 'sight__pk'  # 关联外键

    def get_queryset(self):
        # return Sight.objects.filter(is_valid=True)
        return Info.objects.all()

    def render_to_response(self, context, **response_kwargs):
        """重写响应的返回"""
        page_obj = context['object']
        if page_obj is not None:
            data = serializers.SightInfoSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class TicketDetailView(DetailView):
    """门票详情"""

    def get_queryset(self):
        return Ticket.objects.filter(is_valid=True)

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            data = serializers.TicketDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()
