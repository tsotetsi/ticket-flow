import pytest

from rest_framework.test import APIRequestFactory

from users.models import User
from users.api.views import UserViewSet
from .factories import UserFactory


@pytest.mark.django_db
class TestAPIUserViews:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    @pytest.fixture
    def user(self) -> UserFactory:
        return UserFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request
        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf:APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request
        response = view.me(request)

        assert (response.data == {
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'is_organizer': user.is_organizer,
            'is_customer': user.is_customer,
        })
