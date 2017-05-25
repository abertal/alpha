# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 10:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_group_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='groups',
            field=models.TextField(default=None, null=True, verbose_name='Grupos'),
        ),
        migrations.AlterField(
            model_name='group',
            name='project',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project', verbose_name='Proyecto'),
        ),
    ]
