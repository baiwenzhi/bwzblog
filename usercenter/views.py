# -*- coding: utf-8 -*-
import json
import traceback
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from base.models import Category, Blog, User, Comment, User_visit
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
            blog = Blog.objects.get(id = request.POST.get('id'),user = request.user)
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
    categorys = Category.objects.filter(is_delete = False,user = request.user).order_by('-update_time')
    paginate_datalist_ajax(categorys,len(categorys),request,data,15)
    return render_to_response('center_content/category.html' , data, context_instance=RequestContext(request))

@login_required
def blogs(request):
    data = dict()
    param = dict()
    param['user_id'] = request.user.id
    cursor = connection.cursor()
    cursor.execute(sqls.sql_usercenter_blogs,param)
    dealList =SysUtil.dictfetchall(cursor)

    paginate_datalist_ajax(dealList,len(dealList),request,data,15)
    return render_to_response('center_content/blogs.html' , data, context_instance=RequestContext(request))

@login_required
def write_blog(request):
    data = dict()
    if request.POST.get('blog_id'):
        blog = Blog.objects.get(id=request.POST.get('blog_id'),user = request.user,is_delete=False)
        data['blog']=blog
    categorys = Category.objects.filter(is_delete = False,user = request.user).order_by('-create_time')
    data['categorys'] = categorys
    return render_to_response('center_content/write_blog.html' , data, context_instance=RequestContext(request))

@login_required
def add_category(request):
    data = dict()
    try:
        name = request.POST.get('name')
        Category.objects.create(name = name, user = request.user)
        categorys = Category.objects.filter(is_delete = False,user=request.user)
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
        category = Category.objects.get(id = id,user = request.user)
        category.is_delete = True
        category.save()
        categorys = Category.objects.filter(is_delete = False,user=request.user)
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
        blog = Blog.objects.get(id = id,user = request.user)
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
def comments(request):
    data = dict()
    comments = Comment.objects.filter(blog__is_delete = False,blog__category__is_delete = False,user = request.user,is_delete = False).order_by('-create_time')
    paginate_datalist_ajax(comments,len(comments),request,data,15)
    return render_to_response('center_content/comments_list.html' , data, context_instance=RequestContext(request))


@login_required
def del_comment(request):
    data = dict()
    try:
        id = request.POST.get('id')
        comment = Comment.objects.get(id=id,blog__user=request.user)
        comment.is_delete = True
        comment.save()
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
