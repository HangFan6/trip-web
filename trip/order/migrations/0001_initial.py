# Generated by Django 5.0 on 2024-04-14 16:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_valid", models.BooleanField(default=True, verbose_name="是否有效")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
                ("sn", models.CharField(max_length=32, verbose_name="订单编号")),
                ("buy_count", models.IntegerField(default=1, verbose_name="购买数量")),
                ("buy_amount", models.FloatField(verbose_name="总价")),
                ("to_user", models.CharField(max_length=32, verbose_name="收货人")),
                (
                    "to_area",
                    models.CharField(default="", max_length=32, verbose_name="省市区"),
                ),
                (
                    "to_address",
                    models.CharField(default="", max_length=256, verbose_name="详细地址"),
                ),
                ("to_phone", models.CharField(max_length=32, verbose_name="手机号码")),
                (
                    "remark",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="备注"
                    ),
                ),
                (
                    "express_type",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="快递"
                    ),
                ),
                (
                    "express_num",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="单号"
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(11, "待支付"), (12, "以支付"), (13, "已取消")],
                        default=11,
                        verbose_name="订单状态",
                    ),
                ),
                (
                    "types",
                    models.SmallIntegerField(
                        choices=[(10, "门票"), (11, "酒店")],
                        default=10,
                        verbose_name="订单类型",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "order",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_valid", models.BooleanField(default=True, verbose_name="是否有效")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
                ("flash_name", models.CharField(max_length=128, verbose_name="商品名称")),
                ("flash_img", models.ImageField(upload_to="", verbose_name="商品的主图")),
                ("flash_price", models.FloatField(verbose_name="购买价格")),
                ("flash_origin_price", models.FloatField(verbose_name="原价")),
                ("flash_discount", models.FloatField(verbose_name="折扣")),
                ("count", models.PositiveIntegerField(verbose_name="购买数量")),
                ("amount", models.FloatField(verbose_name="总额")),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(11, "待支付"), (12, "以支付"), (13, "已取消")],
                        default=11,
                        verbose_name="状态",
                    ),
                ),
                (
                    "remark",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="备注"
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="order.order",
                        verbose_name="订单",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "order_item",
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_valid", models.BooleanField(default=True, verbose_name="是否有效")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
                ("amount", models.FloatField(max_length=32, verbose_name="流水号")),
                (
                    "third_sn",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="第三方订单号"
                    ),
                ),
                ("status", models.SmallIntegerField(default=1, verbose_name="支付状态")),
                (
                    "meta",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="其他数据"
                    ),
                ),
                (
                    "remark",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="备注信息"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="order.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "order_payment",
            },
        ),
    ]
