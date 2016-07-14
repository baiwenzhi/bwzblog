from bs4 import BeautifulSoup
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import pylibmc as memcache
from base.models import Blog
import sae.kvdb

def index(request):

    img = sae.kvdb.Client().get('background')
    return render_to_response('base.html',{"background":img} ,context_instance=RequestContext(request))