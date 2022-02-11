from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="patients",
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="doctors",
    )

    description = models.TextField(
        _("description"),
        blank=True,
        unique=False,
        null=True,
        help_text=_("Reason for appointment [optional]."),
    )

    date = models.DateTimeField(_("date"), blank=False, null=False)
    date_created = models.DateTimeField(_("date added"), auto_now_add=True)

    approved = models.BooleanField(
        _("approved"), default=False, null=False, blank=False
    )

    def clean(self) -> None:
        if not self.doctor.is_doctor:
            raise ValidationError(_("mentioned user for doctor is not a doctor"))
        if not self.patient.is_patient:
            raise ValidationError(_("mentioned user for patient is not a patient"))

    def __str__(self) -> str:
        return f"{self.patient}-{self.doctor}-{self.date}"
