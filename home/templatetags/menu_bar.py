from django import template

register = template.Library()

@register.inclusion_tag('menu_bar.html', takes_context=True)
def menu_bar(context):
    return {
        'page': context['page'],
        'user': context['user'],
    }
