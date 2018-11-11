# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-11-11 13:49
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_categorypage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpage',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, verbose_name='аттрибуты'),
        ),
    ]
