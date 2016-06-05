# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20160605_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='duoshuo_logid',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
