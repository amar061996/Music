# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20160421_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songs',
            name='music_file',
            field=models.FileField(upload_to=b''),
        ),
    ]