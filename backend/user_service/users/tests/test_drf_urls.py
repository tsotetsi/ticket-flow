from django.urls import resolve
from django.urls import reverse
from django.test import TestCase

from users.models import User


class TestAPIUserURLS(TestCase):
    def setUp(self):
        self.user =         user = User.objects.create_user(
            email="john@example.com",
            password="something-r@nd0m!",  # noqa: S106
        )

    def test_user_detail(self):
        assert (
            reverse("api:user-detail", kwargs={"pk": self.user.pk}) == f"/api/users/{self.user.pk}/"
        )
        assert resolve(f"/api/users/{self.user.pk}/").view_name == "api:user-detail"


    def test_user_list(self):
        assert reverse("api:user-list") == "/api/users/"
        assert resolve("/api/users/").view_name == "api:user-list"


    def test_user_me(self):
        assert reverse("api:user-me") == "/api/users/me/"
        assert resolve("/api/users/me/").view_name == "api:user-me"