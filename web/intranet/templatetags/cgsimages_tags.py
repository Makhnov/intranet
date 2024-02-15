import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def html_svg(image, class_name=None):
    if hasattr(image, 'svg_html'):
        svg_html = image.svg_html
        if class_name:
            svg_html = re.sub(r'(?i)<svg\s', f'<svg class="{class_name}" ', svg_html, 1)
        return mark_safe(svg_html)
    return ""

@register.simple_tag
def is_svg(image):
    return image.is_svg() if image else False

@register.simple_tag
def icon_name(image):
    return image.title if image else ""
