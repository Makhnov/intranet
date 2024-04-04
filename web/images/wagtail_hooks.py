from wagtail import hooks
from .filters import FilterSvgOperation

@hooks.register("register_image_operations")
def register_image_operations():
    return [("filter_svg", FilterSvgOperation)]

#######################################
##     ICONES DU PANNEAU D'ADMIN     ##
#######################################  

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/law.svg']

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/related.svg']

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/question.svg']

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/answer.svg']

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/choice.svg']

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/minimize.svg']

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/button.svg']