# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe7\x9f\xad\xe5\x90\x8d')),
                ('blog_name', models.CharField(default=None, max_length=100, null=True, verbose_name=b'\xe5\x8d\x9a\xe5\xae\xa2\xe5\x90\x8d', blank=True)),
                ('logo', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Active_Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('url', models.CharField(max_length=200, verbose_name=b'\xe9\x9a\x8f\xe6\x9c\xbaurl')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u9a8c\u8bc1\u90ae\u4ef6',
                'verbose_name_plural': '\u9a8c\u8bc1\u90ae\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='BackgroundImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('img', models.URLField(verbose_name=b'\xe8\x83\x8c\xe6\x99\xaf\xe5\x9b\xbe')),
            ],
            options={
                'verbose_name': '\u80cc\u666f',
                'verbose_name_plural': '\u80cc\u666f',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', blank=True)),
                ('summary', models.TextField(null=True, verbose_name=b'\xe6\x91\x98\xe8\xa6\x81', blank=True)),
                ('content', models.TextField(verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('name', models.CharField(max_length=30, unique=True, null=True, verbose_name=b'name', blank=True)),
                ('fav', models.BooleanField(default=False, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90')),
                ('is_delete', models.BooleanField(default=False)),
                ('visit_count', models.IntegerField(default=0, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe6\xac\xa1\xe6\x95\xb0')),
            ],
            options={
                'verbose_name': '\u535a\u5ba2',
                'verbose_name_plural': '\u535a\u5ba2',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe6\xa0\x8f\xe7\x9b\xae')),
                ('is_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0')),
                ('web_url', models.URLField(max_length=100, null=True, verbose_name=b'', blank=True)),
                ('content', models.TextField(verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x88\xa0\xe9\x99\xa4')),
                ('blog', models.ForeignKey(to='base.Blog')),
                ('parent', models.ForeignKey(default=None, blank=True, to='base.Comment', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='User_visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(default=b'unknown man', max_length=200)),
                ('agent', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('visit_time', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(max_length=64)),
                ('blog', models.ForeignKey(default=None, to='base.Blog', null=True)),
            ],
            options={
                'verbose_name': '\u8bbf\u95ee',
                'verbose_name_plural': '\u8bbf\u95ee',
            },
        ),
        migrations.CreateModel(
            name='WeiboUser',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('uid', models.IntegerField(default=b'unknown man', serialize=False, primary_key=True)),
                ('screen_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xbe\xae\xe5\x8d\x9a\xe5\x90\x8d', blank=True)),
                ('location', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\x9c\xa8\xe5\x9c\xb0', blank=True)),
                ('description', models.CharField(max_length=100, null=True, verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('url', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\x8d\x9a\xe5\xae\xa2\xe5\x9c\xb0\xe5\x9d\x80', blank=True)),
                ('gender', models.CharField(max_length=10, null=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', blank=True)),
                ('access_token', models.CharField(max_length=100, null=True, verbose_name=b'access_token', blank=True)),
                ('profile_url', models.CharField(max_length=200, null=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe7\x9a\x84\xe5\xbe\xae\xe5\x8d\x9a\xe7\xbb\x9f\xe4\xb8\x80URL\xe5\x9c\xb0\xe5\x9d\x80 ', blank=True)),
                ('avatar_large', models.CharField(max_length=200, null=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\xa4\xb4\xe5\x83\x8f\xe5\x9c\xb0\xe5\x9d\x80 ', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(to='base.Category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
