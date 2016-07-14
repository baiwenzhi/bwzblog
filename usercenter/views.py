# -*- coding: utf-8 -*-
import json
import traceback
from bs4 import BeautifulSoup,element
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from base.models import Category, Blog, User, User_visit, Tag, BlogMd
from analysis.models import VisitCount ,VisitCountHour
from base.util import paginate_datalist_ajax, sqls, SysUtil, FileUtil
from django.db import transaction, connection
import datetime

@login_required
def mycenter(request):
    data = dict()
    now_data = datetime.date.today()
    laset_30 = (now_data-datetime.timedelta(days=30))
    data['visit_counts'] = VisitCount.objects.filter(createdate__gt=laset_30).order_by('createdate')
    data['visit_counts_24'] = VisitCountHour.objects.filter(create_time__gt=(datetime.datetime.now()-datetime.timedelta(hours=24))).order_by('create_time')
    return render_to_response('base/base_mycenter.html',data, context_instance=RequestContext(request))

@login_required
def usersetting(request):
    data = dict()
    return render_to_response('center_content/usersetting.html',data, context_instance=RequestContext(request))

@login_required
def fav_blog(request):
    data=dict()
    try:
        with transaction.atomic():
            blog = Blog.objects.get(id = request.POST.get('id'))
            blog.fav = int(request.POST.get('fav'))
            blog.save()
            data['is_succ'] = True

    except Exception as e:
        data['is_succ']=False
        data['msg'] = '设置失败'

    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def categorys(request):
    data = dict()
    categorys = Category.objects.filter(is_delete = False).order_by('-update_time')
    paginate_datalist_ajax(categorys,categorys.count(),request,data,15)
    return render_to_response('center_content/category.html' , data, context_instance=RequestContext(request))

@login_required
def blogs(request):
    data = dict()
    blogs = Blog.objects.select_related('category').filter(is_delete = False).order_by('-create_time')
    paginate_datalist_ajax(blogs,blogs.count(),request,data,15)
    return render_to_response('center_content/blogs.html' , data, context_instance=RequestContext(request))

@login_required
def write_blog(request):
    data = dict()
    if request.POST.get('blog_id'):
        blog = Blog.objects.prefetch_related('tag').select_related('category').get(id=request.POST.get('blog_id'),is_delete=False)
        data['tag_ids'] = ','.join([str(tag.id) for tag in blog.tag.all()])
        data['blog']=blog
    categorys = Category.objects.filter(is_delete = False).order_by('-create_time')
    data['categorys'] = categorys
    data['tags'] = Tag.objects.all()
    return render_to_response('center_content/write_blog.html' , data, context_instance=RequestContext(request))


@login_required
def write_blog_markdown(request):
    data = dict()
    if request.POST.get('blog_id'):
        blog = Blog.objects.prefetch_related('tag').select_related('category').get(id=request.POST.get('blog_id'),is_delete=False)
        data['tag_ids'] = ','.join([str(tag.id) for tag in blog.tag.all()])
        data['blog']=blog
        blogmds = BlogMd.objects.filter(blog=blog)
        if blogmds:
            data['blogmd'] = blogmds[0]
    categorys = Category.objects.filter(is_delete = False).order_by('-create_time')
    data['categorys'] = categorys
    data['tags'] = Tag.objects.all()
    return render_to_response('write_blog.html' , data, context_instance=RequestContext(request))


@login_required
def edit(request):
    data = dict()
    if request.method=='GET':
        categorys = Category.objects.filter(is_delete = False).order_by('-create_time')
        data['categorys'] = categorys
        if request.GET.get('blog_id'):
            blog = Blog.objects.get(id=request.GET.get('blog_id'),is_delete=False)
            data['blog']=blog
            data['tag_ids'] = ','.join([str(tag.id) for tag in blog.tag.all()])
            data['tags'] = Tag.objects.all()
            blogmds = BlogMd.objects.filter(blog=blog)
            if blogmds:
                data['blogmd'] = blogmds[0]
        return render_to_response('edit.html',data, context_instance=RequestContext(request))
    else:
        try:
            id = request.POST.get('id')
            title = request.POST.get('title')
            content = request.POST.get('content')
            tag_ids = request.POST.getlist('taglist[]')
            summary=''
            soup = BeautifulSoup(content)
            tags = []
            listtags = []
            if soup.body:
                listtags = list(soup.body.children)[0:4]
            else:
                listtags = list(soup.children)[0:4]
            for tag in listtags:
                if isinstance(tag,element.Tag):
                    imgtags = tag.find_all('img')
                    for imgtag in imgtags:
                        if 'src' in imgtag.attrs:
                            imgtag['src'] = imgtag.attrs['src']+'!p1'
                tags.append(tag)
            summary = ''.join([tag.encode("utf-8") for tag in tags])
            category_id = request.POST.get('category_id')
            blog = Blog()
            if id != '':
                blog = Blog.objects.get(id=id)
            blog.title=title
            blog.summary=summary
            blog.content=content
            blog.category_id=category_id
            blog.save()
            blog.tag = tag_ids
            if id == '':
                blog.name = SysUtil.random_str(20)+  "-%s.html"%blog.id
                blog.save()
            if request.POST.get('blogmd'):
                BlogMd.objects.update_or_create(blog = blog,content=request.POST.get('blogmd'))
            data['is_succ']=True
        except Exception as e:
            data['is_succ']=False
            data['msg'] = traceback.format_exc()
        return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def add_category(request):
    data = dict()
    try:
        name = request.POST.get('name')
        Category.objects.create(name = name)
        categorys = Category.objects.filter(is_delete = False)
        request.session['categorys'] = categorys
        data['is_succ'] = True
    except Exception:
        data['is_succ'] = False
        data['msg'] = '添加失败'
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def del_category(request):
    data = dict()
    try:
        id = request.POST.get('id')
        category = Category.objects.get(id = id)
        category.is_delete = True
        category.save()
        categorys = Category.objects.filter(is_delete = False)
        request.session['categorys'] = categorys
        data['is_succ'] = True
    except Exception:
        data['is_succ'] = False
        data['msg'] = '删除失败'
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def delete_blog(request):
    data = dict()
    try:
        id = request.POST.get('id')
        blog = Blog.objects.get(id = id)
        blog.is_delete = True
        blog.save()
        data['is_succ'] = True
    except Exception:
        data['is_succ'] = False
        data['msg'] = '删除失败'
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def user_list(request):
    if not request.user.is_superuser:
        raise Http404
    else:
        data = dict()
        users = User.objects.all()
        paginate_datalist_ajax(users,len(users),request,data,15)
        return render_to_response('center_content/userlist.html' , data, context_instance=RequestContext(request))

@login_required
def delete_user(request):
    data = dict()
    if not request.user.is_superuser:
        data['is_succ'] = False
        data['msg'] = '对不起，您没有权限操作'
    else:
        try:
            id = request.POST.get('id')
            user = User.objects.get(id = id,is_superuser = False)
            if user.is_active:
                user.is_active = False
                data['status'] = '已删除'
            else:
                user.is_active = True
                data['status'] = ''
            user.save()
            data['is_succ'] = True
        except Exception:
            data['is_succ'] = False
            data['msg'] = '删除失败'
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def save_logo(request):
    data = dict()
    try:
        request.user.logo = FileUtil.upload_to_upyun(request.FILES['img'])
        request.user.save()
        data['img_url'] = settings.MEDIA_URL+request.user.logo
        data['is_succ'] = True
    except:
        data['is_succ'] = False
        data['msg'] = '修改失败'

    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def save_blog_name(request):
    data = dict()
    try:
        request.user.blog_name = request.POST.get('blog_name')
        request.user.save()
        data['is_succ'] = True
    except:
        data['is_succ'] = False
        data['msg'] = '修改失败'

    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def visit(request):
    data = dict()
    visits = User_visit.objects.all()
    paginate_datalist_ajax(visits,visits.count(),request,data,15)
    return render_to_response('center_content/visit.html' , data, context_instance=RequestContext(request))

@login_required
def add_tag(request):
    data = dict()
    try:
        name = request.POST.get('name')
        tag,created = Tag.objects.get_or_create(name=name)
        if created:
            data['is_succ'] = True
            data['tag_id'] = tag.id
        else:
            data['is_succ'] = False
            data['msg'] = '标签已存在'

    except Exception,e:
        print e
        data['is_succ'] = False
        data['msg'] = '添加失败'

    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
@csrf_exempt
def md_img_upload(request):
    results = dict()
    try:
        photo_keys= request.FILES.keys()
        if len(photo_keys)>0:
            file1=request.FILES[photo_keys[0]]
            size  = file1.size/1024
            limit_num =2000*1000
            if limit_num !=0 and size > limit_num :
                results= {'message': '无法上传超过%sKB图片'%limit_num,'success':0}
            else:
                results= {'message':"上传成功",'url':settings.MEDIA_URL+FileUtil.upload_to_upyun(file1),"success":1}
        else:
            results = {'message': '没有找到图片','success':0}
    except Exception as e:
        pass
    return HttpResponse(json.dumps(results), content_type='application/json')