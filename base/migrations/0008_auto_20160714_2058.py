# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_blogmd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='blog',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='active_email',
            name='user',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='user',
        ),
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
