from django.conf import settings

def wing_context_processor(request):
    my_dict = {
        'LOCAL_HOST': 'http://'+request.META['HTTP_HOST']
    }
    return my_dict