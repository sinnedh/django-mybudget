# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0006_added_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(default=None, max_length=32, null=True, verbose_name='Icon', blank=True),
            preserve_default=True,
        ),
    ]
