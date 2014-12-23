# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mybudget', '0005_expense_is_shared'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('organisation', models.ForeignKey(to='mybudget.Organisation')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='expense',
            name='tags',
            field=models.ManyToManyField(to='mybudget.Tag'),
            preserve_default=True,
        ),
    ]
