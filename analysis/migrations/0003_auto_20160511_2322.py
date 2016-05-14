# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_auto_20160509_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitCountHour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField()),
                ('count', models.IntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe5\x87\xbb\xe6\xac\xa1\xe6\x95\xb0')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u7f51\u7ad9\u70b9\u51fb(\u5c0f\u65f6)',
                'verbose_name_plural': '\u7f51\u7ad9\u70b9\u51fb(\u5c0f\u65f6)',
            },
        ),
        migrations.AlterModelOptions(
            name='visitcount',
            options={'ordering': ['-createdate'], 'verbose_name': '\u7f51\u7ad9\u70b9\u51fb', 'verbose_name_plural': '\u7f51\u7ad9\u70b9\u51fb'},
        ),
    ]
