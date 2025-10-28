from collections.abc import Sequence
from typing import Any

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from factory import Faker
from factory import post_generation
from factory.django import DjangoModelFactory
from rest_framework.test import APIRequestFactory

from users.models import User


class UserFactory(DjangoModelFactory[User]):
    email = Faker("email")
    name = Faker("name")
    phone_number= Faker("phone_number")

    @post_generation
    def password(
        self, create: bool, extracted: Sequence[Any], **kwargs
    ):  # noqa: FBT001
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = User
        django_get_or_create = ["email"]


@pytest.fixture
def api_client_factory():
    return APIClient()

@pytest.fixture
def api_rf() -> APIRequestFactory:
    return APIRequestFactory()

@pytest.fixture()
def url_factory():
    def _url_factory(view_name, *args, **kwargs):
        """
        Factory function to generate URLs dynamically.
        :param view_name: The name of the view to reverse.
        :param args: Positional arguments for the URL pattern.
        :param kwargs: Keyword arguments for the URL pattern.
        :return: The reversed URL.
        """
        return reverse(view_name, args=args, kwargs=kwargs)
    return _url_factory

@pytest.fixture
def user_registration_factory(faker):
    return {
        'email': faker.email(),
        'phone_number': faker.phone_number(),
        'password': faker.password()
    }

@pytest.fixture
def user_factory() -> UserFactory:
    return UserFactory()