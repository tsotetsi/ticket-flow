from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "is_organizer", "is_customer"]

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