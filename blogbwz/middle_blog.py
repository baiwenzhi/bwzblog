"This is the locale selecting middleware that will look at accept headers"
import json

from base.models import User, Category, BackgroundImg
import pylibmc as memcache

class myMiddle(object):
    def process_request(self, request):

        mc = memcache.Client('127.0.0.1')
        visit_count = mc.get("visit_count") or 0
        mc.set('visit_count',int(visit_count)+1)
        if not request.session.has_key('blog_owner'):
            blog_owner = User.objects.get(id = 1,is_active = True)

            request.session['blog_owner'] = blog_owner
            categorys = Category.objects.filter(is_delete = False,user = blog_owner).order_by('-create_time')
            request.session['categorys']=categorys
            backgroundimgs = BackgroundImg.objects.order_by('-create_time')[0:10]
            request.session['backgrounds'] = json.dumps([(bimg.img) for bimg in backgroundimgs])