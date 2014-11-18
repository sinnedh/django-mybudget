# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0004_auto_20141118_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='updated_at',
            field=models.DateTimeField(default=None, auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(default=None, auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='expense',
            name='updated_at',
            field=models.DateTimeField(default=None, auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organisation',
            name='updated_at',
            field=models.DateTimeField(default=None, auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
