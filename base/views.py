# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
import traceback
import datetime

import sys
from django.contrib import auth
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from base.forms import PhotoForm
from base.models import Category , Blog ,User, Active_Email, BackgroundImg, Comment, Tag
from base.util import getUrlRespHtml, paginate_datalist, FileUtil ,SysUtil, \
     send_html_mail, user_visit,sqls, Duoshuo
from django.contrib.auth.decorators import login_required
from django.db import transaction, connection
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from bs4 import BeautifulSoup
import pylibmc as memcache

def index(request):
    data = dict()
    data['menu'] = 'home'
    blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False).order_by('-create_time')
    paginate_datalist(blogs, blogs.count(), request, data, 15)
    return render_to_response('homepage.html',data, context_instance=RequestContext(request))

def get_background(request):
    try:
        redate=getUrlRespHtml('http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')
        redate=json.loads(redate)
        backgroundimg = BackgroundImg()
        backgroundimg.img = redate['images'][0]['url']
        backgroundimg.save()
        return HttpResponse(redate['images'][0]['url'])
    except:
        logging.warning(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def login(request):

    data=dict()
    if request.method == 'GET':
        next = request.GET.get('next')
        data['next'] = next
        backgroundimg = BackgroundImg.objects.order_by('?')[0]
        data['img'] = backgroundimg.img
        return render_to_response('login.html',data, context_instance=RequestContext(request))
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username != '' and password != '':
            try:
                User.objects.get(username=username)
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active == False:
                        data['is_succ'] = False
                        data['msg'] = '用户账号已禁用'
                    else:
                        auth.login(request, user)
                        data['name'] = user.name
                        data['is_succ']=True
                else:
                    data['is_succ']=False
                    data['msg']='账户或密码错误'
            except:
                data['is_succ']=False
                data['msg']='用户不存在'

        return HttpResponse(json.dumps(data), content_type='application/json')

def findpwd(request):
    data = dict()
    if request.method == 'GET':
        urlkey = request.GET.get('urlkey')
        now_three = datetime.datetime.now()-datetime.timedelta(days=3)
        ams = Active_Email.objects.filter(url = urlkey,create_time__gt = now_three)
        if ams:
            backgroundimg = BackgroundImg.objects.all().order_by('-create_time')[0:5]
            data['img'] = backgroundimg[0].img
            data['ams'] = ams[0]
            return render_to_response('changepwd.html',data, context_instance=RequestContext(request))
        else:
            raise Http404
    else:
        email = request.POST.get('email')
        if email != '':
            try:
                users = User.objects.filter(email=email)
                if not users:
                    data['is_succ'] = False
                    data['msg'] = '邮箱不存在'
                elif users[0].is_active is False:
                    data['is_succ'] = False
                    data['msg'] = '账户已失效，请联系管理员'
                else:
                    param = dict()
                    user = users[0]
                    url = SysUtil.random_str(randomlength=20)
                    param['url'] = str(user.id)+url
                    param['host'] = settings.LOCAL_HOST
                    Active_Email.objects.filter(user = user).delete()
                    am = Active_Email()
                    am.user = user
                    am.url = param['url']
                    am.save()
                    send_html_mail('找回密码',loader.render_to_string('template_email/fpwd.html',param),email)
                    data['is_succ'] = True
            except :
                data['is_succ']=False
                data['msg']='发送邮件失败，请联系管理员'
        return HttpResponse(json.dumps(data), content_type='application/json')

def change_pwd(request):
    data = dict()
    pwd = request.POST.get('password')
    urlkey = request.POST.get('urlkey')
    now_three = datetime.datetime.now()-datetime.timedelta(days=3)
    ams = Active_Email.objects.filter(url = urlkey,create_time__gt = now_three)
    if ams:
        user = ams[0].user
        user.set_password(pwd)
        user.save()
        ams[0].delete()
        data['is_succ'] = True
    else:
        data['is_succ'] = False
        data['msg'] = '修改失败'
    return HttpResponse(json.dumps(data), content_type='application/json')

def register(request):
    data = dict()
    username =request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('password')
    name = request.POST.get('name')

    if User.objects.filter(username=username):
        data['is_succ']=False
        data['msg'] = '用户名已存在'
    elif User.objects.filter(email = email,is_active = True):
        data['is_succ']=False
        data['msg'] = '邮箱已注册'
    elif User.objects.filter(name = name,is_active = True):
        data['is_succ']=False
        data['msg'] = '短名已存在'
    else:
        try:
            User.objects.create_user(username=username,email=email,password=password,name=name,blog_name=request.POST.get('blog_name'))
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            param = dict()
            param['user'] = user
            send_html_mail('博客注册成功',loader.render_to_string('template_email/success_register.html',param),email)
            data['name'] = user.name
            data['is_succ']=True
        except :
            data['is_succ'] =False
            data['msg'] = '注册失败'
    return HttpResponse(json.dumps(data), mimetype='application/json')

def logout(request):

    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
@csrf_exempt
def photo_upload(request):
    form = PhotoForm(request.POST,request.FILES)
    results = dict()
    try:
        if form.is_valid():
            file1=form.cleaned_data['photo']
            size  = file1.size/1024
            limit_num =2000*1000
            if limit_num !=0 and size > limit_num :
                results= {'state': '无法上传超过%sKB图片'%limit_num}
            else:
                results= {'url':FileUtil.upload_to_upyun(file1),'title': '', 'state': 'SUCCESS'}
        else:
            results= {'state': '上传失败，图片太大或格式有误'}
    except Exception as e:
        pass
    return HttpResponse(json.dumps(results), mimetype='application/json')


def category(request,category_id):
    data=dict()
    data['category_id'] = int(category_id)
    blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False,category_id=category_id).order_by('-create_time')
    paginate_datalist(blogs, blogs.count(), request, data, 15)
    data['menu']='category'
    return render_to_response('homepage.html',data, context_instance=RequestContext(request))

def blog(request,blog_name):
    data=dict()
    blog_id = blog_name.split('-')[1].split('.')[0]
    blog=Blog.objects.prefetch_related('tag').select_related("category").get(id=blog_id,name=blog_name,is_delete=False)
    data['blog']=blog
    user_visit(request,blog)
    # comments = Comment.objects.filter(blog = blog, is_delete = False, parent = None).order_by('-create_time')
    # data['comments'] = comments
    return render_to_response('blog.html',data, context_instance=RequestContext(request))

def search(request):
    data = dict()
    keywords = request.GET.get('keywords')
    data['keywords'] = keywords
    blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False,title__contains=keywords).order_by('-create_time')
    paginate_datalist(blogs, blogs.count(), request, data, 15)
    data['menu'] = 'home'
    return render_to_response('homepage.html',data, context_instance=RequestContext(request))

@login_required
def edit(request):
    data = dict()
    if request.method=='GET':
        categorys = Category.objects.filter(is_delete = False,user = request.user).order_by('-create_time')
        data['categorys'] = categorys
        if request.GET.get('blog_id'):
            blog = Blog.objects.get(id=request.GET.get('blog_id'),user = request.user,is_delete=False)
            data['blog']=blog
            data['tag_ids'] = ','.join([str(tag.id) for tag in blog.tag.all()])
            data['tags'] = Tag.objects.all()
        return render_to_response('edit.html',data, context_instance=RequestContext(request))
    else:
        try:

            id = request.POST.get('id')
            title = request.POST.get('title')
            content = request.POST.get('content')
            tag_ids = request.POST.getlist('taglist[]')
            summary=''
            soup = BeautifulSoup(content)
            if soup.body:
                summary = ''.join([tag.encode("utf-8") for tag in list(soup.body.children)[0:4]])
            else:
                summary = ''.join([tag.encode("utf-8") for tag in list(soup.children)[0:4]])
            category_id = request.POST.get('category_id')
            blog = Blog()
            if id != '':
                blog = Blog.objects.get(id=id,user = request.user)
            blog.title=title
            blog.user=request.user
            blog.summary=summary
            blog.content=content
            blog.category_id=category_id
            blog.save()
            blog.tag = tag_ids
            if id == '':
                blog.name = SysUtil.random_str(20)+  "-%s.html"%blog.id
                blog.save()
            data['is_succ']=True
        except Exception as e:
            data['is_succ']=False
            data['msg'] = traceback.format_exc()
        return HttpResponse(json.dumps(data), content_type='application/json')

def sub_comment(request):
    data = dict()
    try:
        nickname = request.POST.get('nickname')
        url = request.POST.get('url')
        content = request.POST.get('content')
        comment = Comment()
        blog_name = request.POST.get('blog_name')
        parent_id = request.POST.get('parent_id') or None
        blog = Blog.objects.get(name = blog_name)
        comment.blog = blog
        comment.name = nickname
        comment.content = content
        comment.web_url = url
        comment.parent_id = parent_id
        if request.user.is_authenticated():
            comment.user = request.user
        comment.save()
        data['is_succ'] = True
    except Exception as e:
        data['msg'] = e.message
        data['is_succ'] = False
    return HttpResponse(json.dumps(data), content_type='application/json')

def fav(request):
    data=dict()
    data['menu']='fav'
    blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False,fav=True).order_by('-create_time')
    paginate_datalist(blogs, blogs.count(), request, data, 15)
    return render_to_response('homepage.html',data, context_instance=RequestContext(request))

def timeline(request):
    data=dict()
    data['menu']='timeline'
    blogs = Blog.objects.filter(user = request.session['blog_owner'],is_delete = False).order_by('-create_time').values('title','name','create_time','id')
    paginate_datalist(blogs, len(blogs), request, data, 15)
    return render_to_response('timeline.html',data, context_instance=RequestContext(request))

def tag(request,tag_id):
    data = dict()
    tag = Tag.objects.get(id = tag_id)
    blogs = tag.blog_set.prefetch_related('tag').select_related('category').all()
    paginate_datalist(blogs,blogs.count(),request,data,15)
    return render_to_response('homepage.html',data,context_instance=RequestContext(request))

@csrf_exempt
def return_comment(request):
    user = User.objects.all()[0]
    duoshuo = Duoshuo()
    res = duoshuo.tobu(user.duoshuo_logid)
    logid = user.duoshuo_logid
    if res['code'] == 0:
        if len(res['response'])>0:
            for comlog in res['response']:
                logid=comlog['log_id']
                try:
                    blog = Blog.objects.get(id = comlog['meta']['thread_key'])
                    blog.comment_count += 1
                    blog.save()
                except:
                    continue
            user.duoshuo_logid = logid
            user.save()

    return HttpResponse(json.dumps(res),content_type='application/json')