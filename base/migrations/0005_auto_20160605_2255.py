# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20160517_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '\u6807\u7b7e', 'verbose_name_plural': '\u6807\u7b7e'},
        ),
        migrations.AddField(
            model_name='blog',
            name='comment_count',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\xac\xa1\xe6\x95\xb0'),
        ),
    ]
