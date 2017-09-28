# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Judger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max', models.IntegerField(default=4)),
                ('ip', models.CharField(default=b'0.0.0.0', max_length=30)),
                ('port', models.IntegerField(default=8888)),
                ('remote', models.BooleanField(default=False)),
                ('token', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'judger',
            },
        ),
    ]
