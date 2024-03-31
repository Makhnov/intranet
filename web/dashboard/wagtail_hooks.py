
from django.urls import reverse
from django.utils.html import format_html
from django.templatetags.static import static

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.views.account import BaseSettingsPanel, SettingsTab
from wagtail.admin.views.home import LockedPagesPanel

from users.forms import (
    CustomSettingsForm,
    # UserEditForm,
    # UserCreationForm,
    # CustomUserEditForm,
    # CustomUserCreationForm,
)

from django.utils.translation import gettext_lazy as _

# CSS Panneau admin
@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/dashboard.min.css"))

# JS Panneau admin
@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script type="module" src="{}"></script>', static("js/dashboard.min.js"))

# "Editer son profil de Compte"
custom_tab = SettingsTab("custom",_("Custom settings"), order=300)

# "Editer son profil de Compte"
@hooks.register("register_account_settings_panel")
class CustomSettingsPanel(BaseSettingsPanel):
    name = "custom"
    title =_("My custom settings")
    tab = custom_tab
    order = 100
    form_class = CustomSettingsForm
    template_name = "wagtailadmin/profile/custom_settings.html"

@hooks.register("register_admin_menu_item")
def register_mailing_menu_item():
    return MenuItem(
        _("Mailing"),
        reverse('mailing:index'),
        name="mailing",
        icon_name="mail",
        order=1000,
    )