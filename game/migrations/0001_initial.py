# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-17 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoggleGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_rep', models.CharField(max_length=100)),
                ('words_list', models.TextField()),
                ('winner_name', models.CharField(max_length=32, null=True)),
                ('start_time', models.TimeField(auto_now=True)),
            ],
        ),
    ]
