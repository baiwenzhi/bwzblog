# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_user_duoshuo_logid'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogMd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('content', models.TextField(null=True, verbose_name=b'md\xe5\x86\x85\xe5\xae\xb9', blank=True)),
                ('blog', models.ForeignKey(to='base.Blog')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
