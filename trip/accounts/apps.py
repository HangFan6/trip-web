from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    # Django后台中文显示时，设置的中文名称
    verbose_name = "用户账户"
