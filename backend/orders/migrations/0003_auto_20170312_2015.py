# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 17:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_defaultorder_notified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='defaultorder',
            old_name='adress',
            new_name='address',
        ),
    ]
