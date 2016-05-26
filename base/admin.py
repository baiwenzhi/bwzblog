# coding=utf-8
from django.contrib import admin
from base.models import *
# Register your models here.

class vs_user_visit(admin.ModelAdmin):
    list_display = ('user','visit_time','blog','ip','agent')
    list_filter=('visit_time',)

class vs_category(admin.ModelAdmin):
    list_display = ('name','user','create_time','is_delete')
    list_filter=('create_time',)
    search_fields=('name',)

class vs_blog(admin.ModelAdmin):
    list_display = ('create_time','user','title','category','name','fav','is_delete')
    list_filter=('create_time',)
    search_fields=('title',)

class vs_user(admin.ModelAdmin):
    list_display = ('username','email','date_joined','name','blog_name','logo','is_superuser','is_staff','is_active')
    search_fields=('username',)

class vs_comment(admin.ModelAdmin):
    list_display = ('name','blog','create_time','content','web_url','parent')

class vs_migrationhistory(admin.ModelAdmin):
    list_display = ('app_name','migration','applied')

class vs_img(admin.ModelAdmin):
    list_display = ('img','create_time')

class vs_Active_Email(admin.ModelAdmin):
    list_display = ('url','create_time')

admin.site.register(Category,vs_category)
admin.site.register(Blog,vs_blog)
admin.site.register(User_visit,vs_user_visit)
admin.site.register(User,vs_user)
admin.site.register(Comment,vs_comment)
admin.site.register(BackgroundImg,vs_img)
admin.site.register(Active_Email,vs_Active_Email)
admin.site.register(Tag)
