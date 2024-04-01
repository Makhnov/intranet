from django.urls import reverse, path
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from mailing.views import mailing_view

@hooks.register('register_admin_urls')
def register_mailing_url():
    return [
        path('mailing/', mailing_view, name='mailing'),
    ]
   
@hooks.register('register_permissions')
def register_mailing_permissions():
    return Permission.objects.filter(codename="can_send_mail")
 
@hooks.register("register_admin_menu_item")
def register_mailing_menu_item():
    return MenuItem(
        _("Mailing"),
        reverse('mailing'),
        name="mailing",
        icon_name="mail",
        order=1000,
    )
