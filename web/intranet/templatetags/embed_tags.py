# embed_tags.py
import re
from django import template

register = template.Library()


@register.filter(name="embedurl")
def get_embed_url_with_parameters(embed_value):
    url = embed_value.url  # Accédez à l'URL réelle
    if "youtube.com" in url or "youtu.be" in url:
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"  # Get video id from URL
        embed_url = re.sub(
            regex, r"https://www.youtube.com/embed/\1", url
        )  # Append video id to desired URL
        embed_url_with_parameters = embed_url + "?rel=0"  # Add additional parameters
        return embed_url_with_parameters
    else:
        return None


@register.filter(name="get_css_class")
def get_css_class(value):
    resolution = value.get("resolution")
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
    return value.get("alternative_title", "")
