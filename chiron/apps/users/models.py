from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        validators=[MinLengthValidator(limit_value=5)],
        unique=True,
        blank=False,
        null=False,
        help_text=_("Minimum username length is 5"),
    )

    phone = PhoneNumberField(
        _("phone number"),
        blank=True,
        unique=True,
        null=True,
        help_text=_("Personal phone number [optional]."),
    )
    address = models.TextField(
        _("address"),
        blank=True,
        unique=False,
        null=True,
        help_text=_("Home address [optional]."),
    )

    is_doctor = models.BooleanField(
        _("is doctor"),
        blank=False,
        default=False,
        unique=False,
        null=True,
        help_text=_("Is this person a doctor [default: False]."),
    )

    is_patient = models.BooleanField(
        _("is patient"),
        blank=False,
        default=True,
        unique=False,
        null=True,
        help_text=_("Is this person a patient [default: True]."),
    )

    @property
    def user(self):
        return self

    @property
    def name(self):
        first = f"{self.first_name} "
        return f"{first}{self.last_name}"
