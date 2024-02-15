from wagtail import hooks
from .filters import FilterSvgOperation

@hooks.register("register_image_operations")
def register_image_operations():
    return [("filter_svg", FilterSvgOperation)]