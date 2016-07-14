"This is the locale selecting middleware that will look at accept headers"
import json

from base.models import User, Category, BackgroundImg
import pylibmc as memcache
import  sae.kvdb

class myMiddle(object):
    def process_request(self, request):
        if request.META['PATH_INFO'] in ['/','']:
            kv = sae.kvdb.Client()
            visit_count = kv.get("visit_count") or 0
            kv.set('visit_count',int(visit_count)+1)
        if not request.session.has_key('blog_owner'):
            blog_owner = User.objects.get(id = 1,is_active = True)
            request.session['blog_owner'] = blog_owner


        # if request.META['PATH_INFO'] == '':
        #     mc = memcache.Client(['127.0.0.1'])
        #     visit_count = mc.get("visit_count") or 0
        #     mc.set('visit_count',int(visit_count)+1)
        # if not request.session.has_key('blog_owner'):
        #     blog_owner = User.objects.get(id = 1,is_active = True)
        #     request.session['blog_owner'] = blog_owner
