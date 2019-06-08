# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30, null=True)),
                ('auth_id', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phone_number',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=40, null=True)),
                ('account', models.ForeignKey(to='api.account')),
            ],
        ),
    ]
