# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 18:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20161106_1924'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enrolment',
            unique_together=set([('person', 'group')]),
        ),
    ]