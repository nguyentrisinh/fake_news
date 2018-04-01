# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-01 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler_engine', '0002_newsdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsdetail',
            name='top_image',
        ),
        migrations.AlterField(
            model_name='newsdetail',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Real News'), (2, 'Spam News')], default=1),
        ),
    ]
