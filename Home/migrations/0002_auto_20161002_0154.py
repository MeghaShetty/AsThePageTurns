# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-01 20:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='no_of_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='thread',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 1, 20, 24, 6, 191379, tzinfo=utc)),
        ),
    ]