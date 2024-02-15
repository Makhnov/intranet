# restriction_tags.py
from django import template
from utils.auth import check_page_access

register = template.Library()

@register.simple_tag(takes_context=True)
def authorized_user(context, page, bool=False):
    """ Vérifie si l'utilisateur est autorisé à voir la page """
    user = context['request'].user
    return check_page_access(user, page, bool)

@register.filter
def get_dynamic_attr(obj, attr_name):
    return getattr(obj, attr_name, None)
