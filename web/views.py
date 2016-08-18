from bs4 import BeautifulSoup
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import memcache
from base.models import Blog

def index(request):

    img = memcache.Client(['127.0.0.1']).get('background')
    return render_to_response('base.html',{"background":img} ,context_instance=RequestContext(request))