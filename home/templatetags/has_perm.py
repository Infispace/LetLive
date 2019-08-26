"""
:synopsis: Checks if a user has permission
"""
from django import template

register = template.Library()

@register.simple_tag
def has_perm(user, permission):
    """
    Checks the given user has the given permission.
    
    :param user: the user to check for permissions
    :type user: django.contrib.auth.models.User
    :param str permission: permission to check
    """
    valid = False
    if user.has_perm(permission):
        valid = True

    return valid
