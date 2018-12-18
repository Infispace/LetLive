from django import template

register = template.Library()

@register.simple_tag
def has_perm(user, permission):
    valid = False
    if user.has_perm(permission):
        valid = True

    return valid
