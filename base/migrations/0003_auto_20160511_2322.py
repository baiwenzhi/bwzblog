# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_delete_weibouser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-create_time'], 'verbose_name': '\u535a\u5ba2', 'verbose_name_plural': '\u535a\u5ba2'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-create_time'], 'verbose_name': '\u5206\u7c7b', 'verbose_name_plural': '\u5206\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-create_time'], 'verbose_name': '\u8bc4\u8bba', 'verbose_name_plural': '\u8bc4\u8bba'},
        ),
        migrations.AlterModelOptions(
            name='user_visit',
            options={'ordering': ['-visit_time'], 'verbose_name': '\u8bbf\u95ee', 'verbose_name_plural': '\u8bbf\u95ee'},
        ),
    ]
