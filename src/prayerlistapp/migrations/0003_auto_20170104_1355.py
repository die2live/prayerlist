# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayerlistapp', '0002_auto_20170104_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prayerrequest',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
