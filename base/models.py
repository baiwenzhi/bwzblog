# coding=utf-8
import sys
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser

reload(sys)
sys.setdefaultencoding("utf-8")
from django.db import models

# Create your models here.

class AbstractBaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间", blank=True, null=True, auto_now=True)
    class Meta:
        abstract = True

class User(AbstractUser):
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间", blank=True, null=True, auto_now=True)
    name = models.CharField(verbose_name="短名",max_length=100)
    blog_name = models.CharField(verbose_name="博客名",max_length=100,default=None, blank=True, null=True)
    logo = models.CharField(max_length=100, default=None, blank=True, null=True)
    duoshuo_logid = models.CharField(max_length=50,blank=True)

    def __unicode__(self):
        return self.username

    class Meta:
        db_table='auth_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

class AbstractUserModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间", blank=True, null=True, auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True

class Category(AbstractUserModel):
    name = models.CharField(verbose_name='栏目', max_length=100)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(verbose_name='标签',max_length=50)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __unicode__(self):
        return self.name

class Blog(AbstractUserModel):
    title = models.CharField(verbose_name='标题', max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category)
    summary = models.TextField(verbose_name='摘要',blank=True, null=True)
    content = models.TextField(verbose_name='内容')
    name = models.CharField(verbose_name='name',max_length=30,blank=True, null=True ,unique=True)
    fav = models.BooleanField(verbose_name='推荐',default=False)
    is_delete = models.BooleanField(default=False)
    visit_count = models.IntegerField(verbose_name='浏览次数',default=0)
    tag = models.ManyToManyField(Tag)
    comment_count = models.PositiveIntegerField(verbose_name='评论次数',default=0)

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/blog/%s'%self.name

class User_visit(models.Model):
    user= models.CharField(max_length=200,default='unknown man')
    agent = models.CharField(max_length=200,default=None,null=True,blank=True)
    visit_time=models.DateTimeField(auto_now_add=True)
    ip=models.CharField(max_length=64)
    blog = models.ForeignKey(Blog,default=None,null=True)

    class Meta:
        verbose_name = '访问'
        verbose_name_plural = '访问'
        ordering = ['-visit_time']

    def __unicode__(self):
        return self.user

class Comment(AbstractBaseModel):

    blog = models.ForeignKey(Blog)
    name = models.CharField(verbose_name='昵称',max_length=50)
    web_url = models.URLField(verbose_name='',max_length=100, blank=True, null=True)
    content = models.TextField(verbose_name='内容')
    user = models.ForeignKey(User,default=None,null=True,blank=True)
    parent = models.ForeignKey("self",default=None,null=True,blank=True)
    is_delete = models.BooleanField(verbose_name='是否删除',default=False)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-create_time']
        
    def __unicode__(self):
        return self.id

class Active_Email(AbstractUserModel):
    url = models.CharField(verbose_name='随机url',max_length=200)

    class Meta:
        verbose_name = '验证邮件'
        verbose_name_plural = '验证邮件'

    def __unicode__(self):
        return self.url

class BackgroundImg(AbstractBaseModel):
    img = models.URLField(verbose_name='背景图')

    class Meta:
        verbose_name = '背景'
        verbose_name_plural = '背景'

    def __unicode__(self):
        return self.img
