from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import django.shortcuts as shortcuts
from rest_framework import (
    status,
    viewsets,
    serializers as drf_serializers,
    permissions as drf_permissions,
    mixins,
    decorators,
)
from . import serializers, models
from django.contrib.auth import get_user_model
from django.db.models import Q


class AppointmentViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
):
    """
    APIs for retrieving and managing appointments

    **Permissions**:

    - _Authentication_ is required

    **Actions & Endpoints**:


    * **General Lists** [[/appointment/](/appointment/)]:
        * [`GET`]: lists all appointments for the currently logged-in user
        * [`POST`]: create an appointment for the currently logged-in user
    * **Specific Appointment Managements** [`/appointment/<appointment_id>/`]:
        * **Retrieve** [`GET`]: retrieve details of the specific appointment (if owned by user)
        * **Update** & **Delete**  [`PUT`, `DELETE`]: Update/Remove the specific appointment (if owned by the currently logged-in user as its patient)
    * **Visit Specific Actions**:
        * **Approve** [`/appointment/<appointment_id>/approve/` | `POST`]: approve the specific appointment (if owned by the currently logged-in user as its doctor)
        * **Reject** [`/appointment/<appointment_id>/reject/` | `POST`]: approve the specific appointment (if owned by the currently logged-in user as its doctor)
        * **Visit** [`/appointment/<appointment_id>/visit/` | `GET`]: retireve contact info of doctor if appointment is approved (if appointment is owned by the currently logged-in user as its patient)
    """

    queryset = models.Appointment.objects.all()
    permission_classes = [drf_permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list", "delete"]:
            return serializers.AppointmentSerializer
        if self.action in ["create", "update"]:
            return serializers.AppointmentDoctorSerializer
        return drf_serializers.Serializer

    def filter_queryset(self, queryset):
        if self.action in ["list", "retrieve", "delete"]:
            return queryset.filter(
                Q(doctor=self.request.user) | Q(patient=self.request.user)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.is_valid()
        serializer.save(
            patient=self.request.user,
            doctor=shortcuts.get_object_or_404(
                get_user_model(), username=serializer.validated_data["doctor"]
            ),
        )

    def perform_update(self, serializer):
        self.perform_create(serializer)

    def apply_approval(self, request, toggle, pk=None):
        object = self.get_object()
        if object.doctor == request.user:
            object.approved = toggle
            object.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(methods=["POST"], detail=True, name="Reject Appointments")
    def reject(self, request, pk=None):
        """
        Reject appointment

        **Permissions**:

        * _Authentication_ is required
        * API only available to _Owner_ of the appointment (the doctor)
        """
        return self.apply_approval(request=request, toggle=False, pk=pk)

    @decorators.action(methods=["POST"], detail=True, name="Approve Appointments")
    def approve(self, request, pk=None):
        """
        Approve appointment

        **Permissions**:

        * _Authentication_ is required
        * API only available to _Owner_ of the appointment (the doctor)
        """
        return self.apply_approval(request=request, toggle=True, pk=pk)

    @decorators.action(methods=["GET"], detail=True, name="Visit")
    def visit(self, request, pk=None):
        """
        Get the contact information for appointment

        **Permissions**:

        * _Authentication_ is required
        * API only available to _Owner_ of the appointment (the patient)
        """
        object = self.get_object()
        if object.patient == request.user and object.approved:
            return Response(
                data=dict(phone_number=str(object.doctor.phone)),
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
