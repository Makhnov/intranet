from django.urls import reverse
from django.contrib.auth.models import Permission

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from django.utils.translation import gettext_lazy as _

@hooks.register('register_permissions')
def register_mailing_permissions():
    return Permission.objects.filter(codename="can_send_mail")

@hooks.register("register_admin_menu_item")
def register_mailing_menu_item():
    return MenuItem(
        _("Mailing"),
        reverse('mailing:index'),
        name="mailing",
        icon_name="mail",
        order=1000,
    )
    
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
