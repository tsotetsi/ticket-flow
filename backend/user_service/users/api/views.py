import uuid

from allauth.account.forms import UserTokenForm
from allauth.account.utils import complete_signup, url_str_to_user_pk
from allauth.account.internal import flows
from allauth.account.models import (
    get_emailconfirmation_model,
    EmailAddress
)

from django.http import Http404

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, renderer_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.api.serializers import UserSerializer, RegisterSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from config.settings.base import CONFIRM_EMAIL_ON_GET

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(UserViewSet, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, uuid.UUID)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            complete_signup(request, user, 'mandatory', None) # Trigger email verification
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': RegisterSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomConfirmEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get_object(self, queryset=None):
        key = self.kwargs["key"]
        model = get_emailconfirmation_model()
        email_confirmation = model.from_key(key)
        if not email_confirmation:
            raise Http404()
        return email_confirmation

    def get(self, *args, **kwargs):
        if CONFIRM_EMAIL_ON_GET:
            self.object = verification = self.get_object()
            response = flows.email_verification.verify_email_indirectly(
                self.request,
                verification.email_address.user,
                verification.email_address.user.email
            )
            if response:
                return  Response({
                    "detail": "Email verified successfully.",
                    "data": verification.email_address.user.email
                },
                    status=status.HTTP_200_OK)
        return Response({"detail": "Not accepting GET request on the endpoint"}, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetFromKeyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_user(self, uidb36):
        try:
            uid_int = url_str_to_user_pk(uidb36)
            user = User.objects.get(pk=uid_int)
            if not user:
                return None
            return user
        except(ValueError, User.DoesNotExist):
            return Response({"detail": "Invalid user ID."})

    def get(self, request, uidb36, key, *args, **kwargs):
        # Check if the reset link is valid
        user = self.get_user(uidb36)
        if not user:
            return Response(
                {"detail": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return a response indicating the reset link is valid
        return Response(
            {"detail": "Please submit your new password."},
            status=status.HTTP_200_OK,
        )

    def post(self, request, uidb36, key):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Decode the user ID
            user = self.get_user(uidb36)

            # Validate the reset key.
            token_form = UserTokenForm(data={'uidb36': uidb36, 'key': key})
            if not token_form.is_valid():
                return Response({"detail": "Invalid or expired reset key."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the user email is verified.
            if not EmailAddress.objects.filter(user=user, verified=True).exists():
                return Response({"detail": "Email address not verified."}, status=status.HTTP_400_BAD_REQUEST)

            # Get the new password from the request
            new_password = request.data.get("new_password1")

            # Set the new password
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)