# Generated by Django 4.1 on 2023-05-26 19:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("crawler", "0006_remove_phone_spu_camera_back_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="phone_spu",
            name="phone_id",
        ),
    ]