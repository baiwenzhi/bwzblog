# coding: utf-8
from collections import OrderedDict
import json
import logging
import random
import string
import urllib
import urllib2
import datetime
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import time
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from base.upyun import UpYun, UpYunException
from blogbwz import settings
from blogbwz.settings import EMAIL_HOST_USER
from base.models import Category, User, User_visit

logger = logging.getLogger(__name__)

__author__ = 'bwz'


class sqls():
    sql_blog = '''
                select a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count,count(b.id) as comment_count,c.name as category_name,c.id as category_id
                from base_blog a
                left JOIN base_comment b ON b.blog_id = a.id  and b.is_delete = 0
                 join base_category c on a.category_id = c.id and c.is_delete = 0
                where a.is_delete = 0 and a.user_id = %(user_id)s
                GROUP BY a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count
                order by a.create_time desc
                '''
    sql_search_blog = '''
                    select a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count,count(b.id) as comment_count,c.name as category_name,c.id as category_id
                    from base_blog a
                    left JOIN base_comment b ON b.blog_id = a.id  and b.is_delete = 0
                     join base_category c on a.category_id = c.id and c.is_delete = 0
                    where a.is_delete = 0 and a.user_id = %(user_id)s and a.title like \'%%%(keywords)s%%\'
                    GROUP BY a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count
                    order by a.create_time desc
                    '''
    sql_category_blog = '''
                    select a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count,count(b.id) as comment_count,c.name as category_name,c.id as category_id
                    from base_blog a
                    left JOIN base_comment b ON b.blog_id = a.id  and b.is_delete = 0
                     join base_category c on a.category_id = c.id and c.is_delete = 0
                    where a.is_delete = 0 and a.user_id = %(user_id)s and a.category_id=%(category_id)s
                    GROUP BY a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count
                    order by a.create_time desc
                    '''
    sql_fav_blog = '''
                    select a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count,count(b.id) as comment_count,c.name as category_name,c.id as category_id
                    from base_blog a
                    left JOIN base_comment b ON b.blog_id = a.id and b.is_delete = 0
                     join base_category c on a.category_id = c.id and c.is_delete = 0
                    where a.is_delete = 0 and a.user_id = %(user_id)s and a.fav=%(fav)s
                    GROUP BY a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count
                    order by a.create_time desc
                    '''
    sql_usercenter_blogs = '''
                select a.id,a.create_time,a.title,a.name,a.fav,a.visit_count,count(b.id) as comment_count,c.name as category_name,c.id as category_id
                from base_blog a
                left JOIN base_comment b ON b.blog_id = a.id and b.is_delete = 0
                 join base_category c on a.category_id = c.id and c.is_delete = 0
                where a.is_delete = 0 and a.user_id = %(user_id)s
                GROUP BY a.id,a.create_time,a.title,a.summary,a.content,a.name,a.fav,a.visit_count
                order by a.create_time desc
                '''

def paginate_datalist(dataList, recordNum, request, rtnPara,pageNum=12):
    """
    :rtype : object
    :param dataList:  要分页的数据集合
    :param recordNum: 数据集长度
    :param request:   HttpRequest
    :param rtnPara:   返回的Map Dict
    :param pageNum:   默认12条记录
    """
    paginator = Paginator(dataList, pageNum)  # 每页15行
    paginator._count = recordNum
    page = request.GET.get('page')
    try:
        recList = paginator.page(page)
    except PageNotAnInteger:
        recList = paginator.page(1)
    except EmptyPage:
        recList = paginator.page(paginator.num_pages)
    rtnPara['list_paginator'] = paginator
    rtnPara['record_num'] = recordNum
    rtnPara['recList'] = recList
    querySTRING=request.META['QUERY_STRING'].encode('utf8')
    idxPage = querySTRING.find('page')
    if idxPage == -1:
        rtnPara['prefix'] = '?%s' % querySTRING
    else:
        rtnPara['prefix'] = '?%s' % querySTRING[:idxPage - 1]


def paginate_datalist_ajax(dataList, recordNum, request, rtnPara,pageNum=12):
    """
    :rtype : object
    :param dataList:  要分页的数据集合
    :param recordNum: 数据集长度
    :param request:   HttpRequest
    :param rtnPara:   返回的Map Dict
    :param pageNum:   默认12条记录
    """
    paginator = Paginator(dataList, pageNum)  # 每页15行
    paginator._count = recordNum
    page = request.POST.get('page')
    try:
        recList = paginator.page(page)
    except PageNotAnInteger:
        recList = paginator.page(1)
    except EmptyPage:
        recList = paginator.page(paginator.num_pages)
    rtnPara['list_paginator'] = paginator
    rtnPara['record_num'] = recordNum
    rtnPara['recList'] = recList
    rtnPara['reurl'] = request.META['PATH_INFO']
    querySTRING=request.META['QUERY_STRING'].encode('utf8')
    idxPage = querySTRING.find('page')
    if idxPage == -1:
        rtnPara['prefix'] = '?%s' % querySTRING
    else:
        rtnPara['prefix'] = '?%s' % querySTRING[:idxPage - 1]

def getUrlRespHtml(url):
    heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
            'Accept-Language':'zh-cn,zh;q=0.5',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'John',
            'Keep-Alive':'115',
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    opener.addheaders = heads.items()
    respHtml = opener.open(req).read()
    return respHtml

def getip(ip):
    #使用的易源api的ip查询接口。
    params=dict()
    params['showapi_timestamp']= time.strftime("%Y%m%d%H%M%S", time.localtime())
    params['ip']= ip
    params['appid'] = settings.SHOWAPI.get('appid') or ''
    params['secret'] = settings.SHOWAPI.get('secret') or ''
    url='https://route.showapi.com/20-2?domain=%(ip)s&showapi_appid=%(appid)s&showapi_timestamp=%(showapi_timestamp)s&showapi_sign=%(secret)s'%(params)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    ret_data= json.loads(response.read(),encoding='utf-8')
    dizhi=ret_data['showapi_res_body']['city']
    isp=ret_data['showapi_res_body']['isp']

    return dizhi+','+isp

class DateUtil:
    @classmethod
    def getNowYmdTsp(cls):
        timestr = time.strftime('%y%m%d%H%M%S', time.localtime())
        return timestr

    @classmethod
    def getDayYmdTsp(cls):
        timestr = time.strftime('%y%m%d', time.localtime())
        return timestr

    @classmethod
    def getNow(cls):
        timestr = time.strftime('/%Y/%m/%d/%H%M%S', time.localtime())
        return timestr

class SysUtil:
    #mongo的DB连接
    def __init__(self):
        pass

    @classmethod
    def dictfetchall(cls, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
        # dict(zip([col[0] for col in desc], row))
        OrderedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]

    @classmethod
    def getlucycode(cls):
        str = string.join(random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 6)).replace(' ', '')
        return str

    @classmethod
    def getOrderNo(cls):
        """
        原来取SEQUENCE ,现在改为年月日时分秒加三位随机数
        """
        timeYMD = DateUtil.getNowYmdTsp()
        seq_val =str(random.randint(0, 1000)).zfill(3)
        order_no = '%s%s' % (timeYMD, seq_val)
        return order_no
    @classmethod
    def random_str(cls,randomlength=8):
        a = list(string.ascii_letters)
        random.shuffle(a)
        return ''.join(a[:randomlength])

class FileUtil:
    @classmethod
    def upload_to_upyun(cls, datafile):
        """
        上传图片到又拍去上，返回上传图片的URL链接
        """
        rst_value = random.randint(0,999)
        dtstr = DateUtil.getNow()
        imagename = '%s%s.jpg' % ( dtstr, rst_value)
        logger.info(' imagename >> %s' % imagename)
        upYun = UpYun(settings.UPAN_BUCKETNAME, settings.UPAN_USERNAME, settings.UPAN_USERPASS)
        upYun.setApiDomain('v1.api.upyun.com')
        #开启调试，默认关闭调试
        upYun.debug = settings.UPAN_IS_DEBUG

        a = upYun.writeFile(path=imagename, data=datafile, auto=True)
        return imagename

    @classmethod
    def delete_from_upyun(cls, imagename):
        """
        上传图片到又拍去上，返回上传图片的URL链接
        """
        upYun = UpYun(settings.UPAN_BUCKETNAME, settings.UPAN_USERNAME, settings.UPAN_USERPASS)
        upYun.setApiDomain('v1.api.upyun.com')
        #开启调试，默认关闭调试
        upYun.debug = settings.UPAN_IS_DEBUG

        try:
            status = upYun.deleteFile(imagename)
            logger.info(' delete succ %s ' % imagename)
        except UpYunException:
            logger.error(' delete fail %s' % imagename)
        finally:
            status = False
        return status

def send_html_mail(subject, html_content, recipient_list):
    li=[]
    if type(recipient_list) != list:
        li.append(recipient_list)
    else:
        li = recipient_list
    msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, li)
    msg.content_subtype = "html" # Main content is now text/html
    msg.send()

def sendmail(title,message,recv):
    sender= EMAIL_HOST_USER
    mail_list=[]
    mail_list.append(recv)
    send_mail(
                subject=title,
                message=message,
                from_email=sender,
                recipient_list=mail_list,
                fail_silently=False,
                connection=None
            )

def user_visit(request,blog):
    #统计用户访问情况。
    try:
        agent =request.META['HTTP_USER_AGENT']
        if agent.find('baidu')>=0 or agent.find('bot')>=0 or agent.find('pider')>=0:
            pass
        else:
            visit_data = request.session.get('visit_data') or []
            if isinstance(visit_data,str):
                visit_data = []
            if blog.id in visit_data:
                pass
            else:
                visit_data.append(blog.id)
                request.session['visit_data'] = visit_data
                blog.visit_count +=1
                blog.save()
                sip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
                ip = str(sip).split(',')[0]
                weizhi = getip(ip) + ',' + ip
                User_visit.objects.create(ip=weizhi, agent=agent, blog=blog)
    except:
        pass