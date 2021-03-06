# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_volunteer_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.TextField(verbose_name='Nombre proyecto')),
                ('date_start', models.DateField(verbose_name='Fecha inicio')),
                ('date_end', models.DateField(verbose_name='Fecha fin')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Observaciones')),
            ],
            options={
                'verbose_name': 'Proyecto',
            },
        ),
    ]
