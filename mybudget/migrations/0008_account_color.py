# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0007_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='color',
            field=models.CharField(default=b'#3388CD', max_length=32, null=True, verbose_name='Color', blank=True),
            preserve_default=True,
        ),
    ]
