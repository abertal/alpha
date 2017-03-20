# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personmembership',
            name='membership',
        ),
        migrations.RemoveField(
            model_name='personmembership',
            name='person',
        ),
        migrations.AddField(
            model_name='membership',
            name='card_status',
            field=models.TextField(blank=True, default='', verbose_name='Estado del carnet'),
        ),
        migrations.AddField(
            model_name='membership',
            name='dpa_status',
            field=models.TextField(blank=True, default='', verbose_name='LOPD'),
        ),
        migrations.AddField(
            model_name='membership',
            name='id_card_status',
            field=models.TextField(blank=True, default='', verbose_name='DNI/NIE'),
        ),
        migrations.AddField(
            model_name='membership',
            name='photo_status',
            field=models.TextField(blank=True, default='', verbose_name='Foto'),
        ),
        migrations.AddField(
            model_name='membership',
            name='ss_card_status',
            field=models.TextField(blank=True, default='', verbose_name='Tarjeta sanitaria'),
        ),
        migrations.DeleteModel(
            name='PersonMembership',
        ),
    ]
