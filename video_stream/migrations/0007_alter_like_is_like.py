# Generated by Django 4.2.7 on 2023-11-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_stream', '0006_like_is_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='is_like',
            field=models.BooleanField(default=False),
        ),
    ]