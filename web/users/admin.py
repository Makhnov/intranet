from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ["pk", "email", "username", "first_name", "last_name", "is_staff", "is_active"]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "civility",
                    "date_of_birth",
                    "address1",
                    "address2",
                    "zip_code",
                    "city",
                    "mobile_phone",
                    "municipality",
                    "function_municipality",
                    "function_council",
                    "commission",
                    "function_commission",
                    "function_bureau",
                    "function_conference"
                )
            },
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "civility",
                    "date_of_birth",
                    "address1",
                    "address2",
                    "zip_code",
                    "city",
                    "mobile_phone",
                    "municipality",
                    "function_municipality",
                    "function_council",
                    "commission",
                    "function_commission",
                    "function_bureau",
                    "function_conference"
                )
            },
        ),
    )


admin.site.register(User, UserAdmin)
