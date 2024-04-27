# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/8 
"""
from system.serializers import BaseImageSerializer
from utils.serializers import BaseListPageSerializer, BaseSerializer


class SightListSerializer(BaseListPageSerializer):
    """景点列表"""

    def get_objects(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'main_img': obj.main_img.url,
            'score': obj.score,
            'province': obj.province,
            'city': obj.city,
            'area': obj.area,
            'min_price': obj.min_price,
            # TODO 评论数量暂时无法获取
            'comment_count': obj.comment_count
        }


class SightDetailSerializer(BaseSerializer):
    """景点详情"""

    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'img': obj.banner_img.url,
            'content': obj.content,
            'score': obj.score,
            'province': obj.province,
            'city': obj.city,
            'area': obj.area,
            'town': obj.town,
            'min_price': obj.min_price,
            # TODO 评论数量暂时无法获取
            'comment_count': obj.comment_count,
            'image_count': obj.image_count
        }


class CommentListSerializer(BaseListPageSerializer):
    """评论列表"""

    def get_objects(self, obj):
        user = obj.user
        images = []
        for image in obj.images.filter(is_valid=True):
            images.append(BaseImageSerializer(image).to_dict())
        return {
            'user': {
                'pk': user.pk,
                'nickname': user.nickname
            },
            'pk': obj.pk,
            'content': obj.content,
            'is_top': obj.is_top,
            'love_count': obj.love_count,
            'score': obj.score,
            'is_public': obj.is_public,
            'images': images,
            'created_at': obj.created_at.strftime('%Y-%m-%d')
        }


class TicketListSerializer(BaseListPageSerializer):
    """门票列表"""

    def get_objects(self, obj):
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.price,
            'discount': obj.discount,
            'sale_price': obj.sale_price,
            'total_stock': obj.total_stock,
            'remain_stock': obj.remain_stock
        }


class SightInfoSerializer(BaseSerializer):
    """景点介绍"""

    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.sight.pk,  # 景点ID
            'entry_explain': obj.entry_explain,
            'play_way': obj.play_way,
            'tips': obj.tips,
            'traffic': obj.traffic,
        }


class TicketDetailSerializer(BaseSerializer):
    """门票详情"""

    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.types,
            'sale_price': obj.sale_price,
            # 显示字典内容
            'entry_way': obj.get_entry_way_display(),
            'tips': obj.tips,
            'remark': obj.remark
        }
