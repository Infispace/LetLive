"""
:synopsis: Checks if the environment is in debug mode
"""
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def is_debug():
    """
    Checks if the DEBUG variable in setting.py is "True"
    """
    return settings.DEBUG

