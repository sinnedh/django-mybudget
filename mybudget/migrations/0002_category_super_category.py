# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='super_category',
            field=models.ForeignKey(default=None, blank=True, to='mybudget.Category', null=True),
            preserve_default=True,
        ),
    ]
