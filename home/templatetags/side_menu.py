"""
:synopsis: passes context to side_menu.html template
"""
from django.urls import reverse
from django import template

register = template.Library()

@register.simple_tag
def render_side_menu(page):
    """
    Checks if page should render side menu
    
    :param page : page from urls.py
    """
    render_menu = False
    # set profile page side menu
    if (page == 'user_profile' 
        or page == 'user_profile_edit'
        or page == 'user_subscription'
        or page == 'password_change'
        or page == 'password_change_done'
    ):
        render_menu = True
        
    # set users page side menu
    if (page == 'user_default' 
        or page == 'user_new'
        or page == 'user_admin'
        or page == 'user_author'
        or page == 'user_subscriber'
        or page == 'user_view'
        or page == 'user_delete'
    ):
        render_menu = True

    # return
    return render_menu

@register.inclusion_tag('side_menu.html', takes_context=True)
def side_menu(context):
    """
    Passes `menu_links` to template `side_menu.html`.
    The `menu_links` is an array of json objects with the following attributes.
    
    ::
    
      {
        'url' : 'link target url',
        'text' : 'the text to display in the menu link',
        'active_page' : 'the page which the menu link is active',
      }
      
    Also passes `'page' : 'page from urls.py',` to the template.
    """
    page = context['page']
    menu_links = []

    # set profile page side menu
    if (page == 'user_profile'
        or page == 'user_profile_edit'
        or page == 'user_subscription'
        or page == 'password_change'
        or page == 'password_change_done'
    ):
        view_profile = {
            'url' : reverse('home:user_profile'),
            'text' : 'View Profile',
            'active_page' : 'user_profile',
        }
        
        edit_profile = {
            'url' : reverse('home:user_profile_edit'),
            'text' : 'Edit Profile',
            'active_page' : 'user_profile_edit',
        }
        
        subscription = {
            'url' : reverse('home:user_subscription'),
            'text' : 'My Subscription',
            'active_page' : 'user_subscription',
        }
        
        change_password = {
            'url' : reverse('home:password_change'),
            'text' : 'Change Password',
            'active_page' : 'password_change',
        }
        
        menu_links = [
            view_profile,
            edit_profile,
            subscription,
            change_password,
        ]

    # set users page side menu
    if (page == 'user_default' 
        or page == 'user_new'
        or page == 'user_admin'
        or page == 'user_author'
        or page == 'user_subscriber'
        or page == 'user_view'
        or page == 'user_delete'
    ):
        all_users = {
            'url' : reverse('home:user_default'),
            'text' : 'All Users',
            'active_page' : 'user_default',
        }
        
        admins = {
            'url' : reverse('home:user_admin'),
            'text' : 'Administrators',
            'active_page' : 'user_admin',
        }
        
        authors = {
            'url' : reverse('home:user_author'),
            'text' : 'Authors',
            'active_page' : 'user_author',
        }
        
        subscribers = {
            'url' : reverse('home:user_subscriber'),
            'text' : 'Subscribers',
            'active_page' : 'user_subscriber',
        }
        
        add_new = {
            'url' : reverse('home:user_new'),
            'text' : 'Add New User',
            'active_page' : 'user_new',
        }
        
        menu_links = [
            all_users,
            authors,
            subscribers,
            admins,
            add_new,
        ]
        
    # set topics page side menu
    if (page == 'topic_default'
        or page == 'topic_view'
        or page == 'topic_new'
        or page == 'topic_edit'
        or page == 'topic_delete'
    ):
        all_topics = {
            'url' : reverse('home:topic_default'),
            'text' : 'All Topics',
            'active_page' : 'topic_default',
        }
        
        new_topic = {
            'url' : reverse('home:topic_new'),
            'text' : 'New Topic',
            'active_page' : 'topic_new',
        }
        
        menu_links = [
            all_topics,
            new_topic,
        ]
    
    return {
        'page': page,
        'menu_links': menu_links,
    }

