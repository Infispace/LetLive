"""
:synopsis: passes context to nav_branding.html template
"""
from django import template

register = template.Library()

@register.inclusion_tag('nav_branding.html', takes_context=True)
def nav_branding(context, url=None):
    """
    Passes context to template `nav_branding.html`.    
    ::
    
      {'site_url' : 'the site url'}
    """
    if url is None:
        url = 'http://127.0.0.1:8000/'
        
    return {'site_url': url}
