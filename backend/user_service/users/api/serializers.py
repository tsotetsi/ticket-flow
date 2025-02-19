from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from allauth.account.forms import ResetPasswordForm
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "name", "email", "phone_number", "is_organizer", "is_customer"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "pk"}}


class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("name", "email", "phone_number", "password", "is_customer", "is_organizer")

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Check if the email exists in the database.
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("use with this email address does not exist.")
        return value

    def save(self, **kwargs):
        request = self.context.get('request')
        form = ResetPasswordForm(data=self.validated_data)
        if form.is_valid():
            form.save(request=request)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_new_password1(self, value):
        try:
            # Validate the new password against the validators in base.py.
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data