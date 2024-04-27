from django.apps import AppConfig


class SightConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sight"
    # Django后台中文显示时，设置的中文名称
    verbose_name = "景点模块"
