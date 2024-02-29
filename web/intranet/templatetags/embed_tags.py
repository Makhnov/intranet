# embed_tags.py
import re
from django import template

register = template.Library()


@register.filter(name="embedurl")
def get_embed_url_with_parameters(embed_value):
    if hasattr(embed_value, 'url'):
        url = embed_value.url 
        if "youtube.com" in url or "youtu.be" in url:
            regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
            embed_url = re.sub(regex, r"https://www.youtube.com/embed/\1", url)
            embed_url_with_parameters = embed_url + "?rel=0"
            return embed_url_with_parameters
    return None



@register.filter(name="get_css_class")
def get_css_class(value):

    if isinstance(value, dict):
        resolution = value.get("resolution")
    else:
        resolution = None

    css_classes = {
        "very_small": "embed-very-small",
        "small": "embed-small",
        "medium": "embed-medium",
        "large": "embed-large",
        "very_large": "embed-very-large",
    }
    return css_classes.get(resolution, "embed-medium")


@register.filter(name="get_alternative_title")
def get_alternative_title(value):
    if isinstance(value, dict):
        return value.get("alternative_title", "")
    else:
        return ""
