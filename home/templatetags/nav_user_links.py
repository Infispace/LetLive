"""
:synopsis: passes context to `nav_login_form.html` and `nav_user_btn.html` templates
"""
from django import template
from home.forms import LoginForm

register = template.Library()

@register.inclusion_tag('nav_login_form.html', takes_context=True)
def nav_login_form(context, api=False):
    """
    Passes context to template `base_login_form.html`.    
    ::
    
      {
        'user': 'authenticated user',
        'login_form': 'user login form',
      }
    """
    form = LoginForm()
    user = context['user']
    
    return {
        'user': user,
        'login_form': form,
    }
    
@register.inclusion_tag('nav_user_btn.html', takes_context=True)
def nav_user_btn(context, api=False):
    """
    Passes context to template `base_login_form.html`.    
    ::
    
      {'user': 'authenticated user'}
    """
    user = context['user']
    
    return {'user': user}
