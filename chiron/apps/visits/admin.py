from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class AppointmentAdmin(admin.ModelAdmin):
    verbose_name = _("appointment")
    verbose_name_plural = _("appointments")
    model = models.Appointment
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "patient",
                    "doctor",
                    "date_created",
                    "description",
                    "date",
                    "approved",
                )
            },
        ),
    )
    autocomplete_fields = ["patient", "doctor"]
    read_only_fields = ["picture"]
    search_fields = [
        "patient__username",
        "patient__phone",
        "patient__email",
        "patient__first_name",
        "patient__last_name",
        "doctor__username",
        "doctor__phone",
        "doctor__email",
        "doctor__first_name",
        "doctor__last_name",
    ]
    readonly_fields = ["date_created"]
    list_display = ["patient", "doctor", "date", "approved"]
    can_delete = True


admin.site.register(models.Appointment, AppointmentAdmin)
