# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitcount',
            name='id',
        ),
        migrations.AlterField(
            model_name='visitcount',
            name='createdate',
            field=models.DateField(auto_now_add=True, serialize=False, primary_key=True),
        ),
    ]
