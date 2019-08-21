"""
:synopsis: passes context to base_login_form.html template
"""
from django import template
from home.forms import LoginForm

register = template.Library()

@register.inclusion_tag('base_login_form.html', takes_context=True)
def base_login_form(context):
    """
    Passes context to template `base_login_form.html`.    
    ::
    
      {
        'login_form' : 'user login form',
      }
    """
    form = LoginForm()
    return {'login_form': form}
