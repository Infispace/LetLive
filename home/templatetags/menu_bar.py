"""
:synopsis: passes context to menu_bar.html template
"""
from django import template

register = template.Library()

@register.inclusion_tag('menu_bar.html', takes_context=True)
def menu_bar(context):
    """
    Passes context to template.    
    ::
    
      {
        'page' : 'page from urls.py',
        'user' : 'the authenticated user'
      }
    """
    return {
        'page': context['page'],
        'user': context['user'],
    }
