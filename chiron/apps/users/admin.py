from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy
from rest_framework.authtoken.admin import TokenAdmin as DRF_TokenAdmin
from . import models

# website configurations
admin.site.site_header = _("Chiron Administration")
admin.site.site_title = _("Chrion")
admin.site.index_title = _("Chiron Management")


class TokenAdmin(DRF_TokenAdmin):
    model = TokenProxy
    verbose_name = _("Token")
    verbose_name_plural = _("Tokens")
    autocomplete_fields = ["user"]
    fields = ["user", "key", "created"]
    readonly_fields = ["key", "created"]
    list_view = ["user__username", "key", "created"]
    can_delete = True


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "phone", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "address")},
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "user_permissions"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "phone",
                    "email",
                    "first_name",
                    "last_name",
                    "address",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")


admin.site.unregister(AuthGroup)
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, TokenAdmin)
admin.site.register(models.User, UserAdmin)
