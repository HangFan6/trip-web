# Generated by Django 5.0 on 2024-04-09 15:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("sight", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Common",
            new_name="Comment",
        ),
    ]