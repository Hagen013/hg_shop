# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='главное изображение')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='media/thumb', verbose_name='thumbnail')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ProductPage', verbose_name='товар')),
            ],
        ),
    ]
