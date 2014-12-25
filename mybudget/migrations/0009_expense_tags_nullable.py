# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0008_account_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='tags',
            field=models.ManyToManyField(default=None, to='mybudget.Tag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
