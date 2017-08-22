import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from experchat.authentication import TokenAuthentication

User = get_user_model()


@pytest.mark.django_db
class TestTokenAuthentication(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create(email='testuser@example.com', is_email_verified=True)

    def test_token_auth(self):
        # Create an instance of a GET request for creating auth_token.
        request = self.factory.get('/')

        user = User.objects.get(email='testuser@example.com')
        token = TokenAuthentication.generate_credentials(request, user.id)

        # Generate Authorization header to create request for authentication.
        authorization_header = "Token {token}".format(token=token)

        # Create an instance of a GET request for validating auth_token.
        auth_request = self.factory.get('/', HTTP_AUTHORIZATION=authorization_header)

        # Authenticate auth request
        auth_data = TokenAuthentication().authenticate(auth_request)

        assert auth_data[0] == user
