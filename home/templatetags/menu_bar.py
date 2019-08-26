"""
:synopsis: passes context to menu_bar.html template
"""
from django import template

register = template.Library()

@register.inclusion_tag('menu_bar.html', takes_context=True)
def menu_bar(context):
    """
    Passes context to template `menu_bar.html`.
    ::
    
      {
        'page' : 'page from urls.py',
        'user' : 'the authenticated user'
      }
    """
    page = context['page']
    # set users menu item
    if (page == 'user_default' 
        or page == 'user_new'
        or page == 'user_author'
        or page == 'user_publisher'
        or page == 'user_view'
        or page == 'user_delete'
    ):
        page = 'users'
        
    # set my blog menu item
    if page == 'my_blog' or page == 'article_filter':
        page == 'my_blog'
    
    return {
        'page': page,
        'user': context['user'],
    }
