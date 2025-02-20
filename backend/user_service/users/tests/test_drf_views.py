import pytest
import jwt
from unittest.mock import patch
from django.conf import settings
from rest_framework.test import APIRequestFactory

from users.models import User
from users.api.views import UserViewSet
from .factories import UserFactory, url_factory, api_rf, api_client_factory, user_factory, user_registration_factory


@pytest.mark.django_db
class TestAPIUserViews:
    @pytest.fixture
    def user(self) -> UserFactory:
        return UserFactory()

    def test_get_queryset(self, user_factory: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user_factory

        view.request = request
        assert user_factory in view.get_queryset()

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


class TestRegisterView:
    def test_register_url(self, url_factory):
        register_url = url_factory("register")
        assert register_url == "/api/register"

    @patch('allauth.account.utils.complete_signup')  # Mock the complete_signup function
    @pytest.mark.django_db
    def test_user_registration_success(self, mock_complete_signup, api_client_factory, url_factory, user_registration_factory):
        response = api_client_factory.post(url_factory('register'), user_registration_factory)
        assert response.status_code == 201

        # Check if user data was set properly.
        assert 'user' in response.data
        assert response.data['user']['email'] == user_registration_factory['email']
        assert response.data['user']['phone_number'] == user_registration_factory['phone_number']

        # Check if the response contains access token and refresh token
        assert 'refresh' in response.data
        assert response.data['refresh'] is not None
        assert 'access' in response.data
        assert response.data['access'] is not None

        # Decode and verify the access token
        access_token = response.data['access']
        try:
            decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            pytest.fail("The access token has expired.")
        except jwt.InvalidTokenError:
            pytest.fail("The access token is invalid.")

        # Verify the token payload and is of the correct user.
        assert decoded_token['user_id'] == response.data['user']['id']
        assert 'exp' in decoded_token  # Ensure expiration claim is present