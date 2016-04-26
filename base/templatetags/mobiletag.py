#coding:utf-8
from django import template
from base.models import Comment

register=template.Library()

@register.tag(name="get_pagination_pages")
def get_pagination_pages(parser, token):
    try:
        tag_name,page,page_nums = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one arguments" % token.contents.split()[0])
    return do_get_pages(page,page_nums)

class do_get_pages(template.Node):
    def __init__(self,page,page_nums):
        self.page = template.Variable(page)
        self.page_nums = template.Variable(page_nums)
    def render(self, context):
        page=self.page.resolve(context)
        page_nums=self.page_nums.resolve(context)
        ranges=[]
        if page_nums<=10:
            ranges=range(1,page_nums+1)
        elif page_nums>10  and page<=5:
            ranges=range(1,11)
        elif page_nums>10 and page>=page_nums-5:
            ranges=range(page_nums-9,page_nums+1)
        else:
            ranges=range(page-4,page+6)

        context['range']=ranges
        return  ''

@register.tag(name="get_child_comment")
def get_child_comment(parser, token):
    try:
        tag_name,comment = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one arguments" % token.contents.split()[0])
    return do_get_child_comment(comment)

class do_get_child_comment(template.Node):
    def __init__(self,comment):
        self.comment = template.Variable(comment)
    def render(self, context):
        comment = self.comment.resolve(context)
        child_comments = Comment.objects.filter(parent = comment, is_delete = False).order_by('-create_time')
        context['child_comments']=child_comments
        return  ''

