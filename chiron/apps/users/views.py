from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import django.shortcuts as shortcuts
from rest_framework.decorators import action
from rest_framework import (
    status,
    viewsets,
    serializers as drf_serializers,
    permissions as drf_permissions,
    mixins,
)
from . import serializers, models, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.mail import send_mail
from django.conf import settings


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    API for user information management and retrieval

    * **Login** [[/user/login/](/user/login/) | `POST`]: obtain a valid authentication token by sending valid credentials
    * **Logout** [[/user/logout/](/user/logout/) | `POST`]: invalidate currently owned authentication token
    * **Retrieve User** [`/user/<username>/` | `GET`]: obtain user information (by looking up username)
    * **Doctors** [[/user/drs/](/user/drs/) | `GET`]: get the list of all doctors
    * **Profile Management** [[/user/me/](/user/me/)]:
        * [`PUT`]: update ego user's information (excluding the password)
        * [`GET`]: obtain current user information
    * **Change Password** [/user/cpw/](/user/cpw/) | `POST`]: update user password (old password is required)
    """

    lookup_field = "username"
    lookup_url_kwarg = "username"
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = serializers.EgoUserSerializer
    queryset = models.User.objects.all()

    def get_view_name(self):
        return getattr(self, "name", "User") or "User"

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.RegistrationSerializer
        if self.action in ["retrieve", "update", "me", "list"]:
            if self.request.user.is_staff or (
                "username" in self.request.parser_context["kwargs"]
                and self.request.user.username
                == self.request.parser_context["kwargs"]["username"]
            ):
                return serializers.EgoUserSerializer
            else:
                return serializers.UserSerializer
        elif self.action == "cpw":
            return serializers.ChangePasswordSerializer
        elif self.action == "login":
            return AuthTokenSerializer
        elif self.action == "logout":
            return drf_serializers.Serializer
        elif self.action == "invite":
            return serializers.InviteSerializer
        return serializers.UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["create", "login"]:
            permission_list = [drf_permissions.AllowAny]
        elif self.action in ["update", "pw", "logout", "me"]:
            permission_list = [
                permissions.IsSelfOrAdmin,
                drf_permissions.IsAuthenticated,
            ]
        elif self.action in ["retrieve", "list", "invite"]:
            permission_list = [drf_permissions.IsAuthenticated]
        else:
            permission_list = [drf_permissions.AllowAny]
        return [permission() for permission in permission_list]

    @action(methods=["GET", "PUT"], detail=False, name="Profile Management")
    def me(self, request):
        """
        Retrieve and change the current user's account information.

        **Permissions**:

        * _Authentication_ is required
        * API only available to _Owner_ of the account
        """
        if request.method == "GET":
            self.kwargs["username"] = request.user.username
            return self.retrieve(request)
        elif request.method == "PUT":
            self.kwargs["username"] = request.user.username
            return self.update(request)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=False, name="Doctors")
    def drs(self, request):
        """
        Retrieve the list of all doctors.

        **Permissions**:

        * _Authentication_ is required
        """

        doctors = models.User.objects.filter(is_doctor=True)

        return Response(self.get_serializer_class()(doctors, many=True).data)

    @action(methods=["POST"], detail=False, name="Change Password")
    def cpw(self, request, format=None):
        """
        Change user's passcode API by providing the old password.

        **Permissions**:

        * _Authentication_ is required
        * API only available to _Admins_ or the _Owner_ of the account
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response(
                    {"new_password": ["New passwords must match"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.object.save()
            return Response(
                {"response": "successfully changed password"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        detail=False,
    )
    def login(self, request, format=None):
        """
        Obtain an authentication token by providing valid credentials.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.is_active:  # todo: handle account activation
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

    @action(
        methods=["POST"],
        detail=False,
    )
    def logout(self, request, format=None):
        """
        Invalidate the currently owned authentication token.

        **Permissions** :

        * _Authentication_ is required
        """
        shortcuts.get_object_or_404(Token, user=request.user).delete()
        return Response(status=status.HTTP_202_ACCEPTED)
