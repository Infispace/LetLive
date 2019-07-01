from django import template
from home.models import Subscriber
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()
    
@register.simple_tag(name="view_blog_menu")
def view_blog_menu(user):
    view = True

    try:
        if user.groups.filter(name='Administrators').exists():
            view = False
            
        elif user.groups.filter(name='Subscribers').exists():
            sub = Subscriber.objects.get(user_id=user.id)
          
            if sub.subscription_type == Subscriber.FREE:
                view = False
    except ObjectDoesNotExist as e:
        pass
                
    return view
