from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(allow_null=False)
    doctor = serializers.CharField(allow_null=False)

    class Meta:
        model = models.Appointment
        fields = "__all__"
        read_only_fields = ["approved"]

    def validate(self, attrs):
        try:
            if get_user_model().objects.get(username=attrs["doctor"]).is_doctor:
                return super().validate(attrs)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "mentioned user for doctor does not exist"
            )
        raise serializers.ValidationError("mentioned user for doctor is not a doctor")


class AppointmentDoctorSerializer(AppointmentSerializer):
    doctor = serializers.CharField(allow_null=False)

    class Meta:
        model = models.Appointment
        fields = ["id", "doctor", "description", "date"]
        read_only_fields = ["id"]
