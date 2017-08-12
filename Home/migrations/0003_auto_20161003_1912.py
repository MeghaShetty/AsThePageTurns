# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-03 13:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20161002_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='prologue',
            field=models.TextField(default='No Prologue available', max_length=1000),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='chapter_content',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 3, 13, 42, 58, 715483, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
