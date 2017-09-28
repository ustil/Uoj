# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judger',
            name='port',
            field=models.IntegerField(default=8888, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='judger',
            name='token',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
