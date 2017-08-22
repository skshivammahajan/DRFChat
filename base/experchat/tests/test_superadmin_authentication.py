import pytest
from django.conf import settings
from django.test import RequestFactory, TestCase
from rest_framework.exceptions import AuthenticationFailed

from experchat.authentication import SuperAdminAuthentication


class TestSuperAdminAuthentication(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        settings.WP_SUPER_ADMIN_TOKEN = '2m#pi1x)175ekzji-&*3s^a$1l=*xo06$4#)bdj4%!dqp-)*mu'
        settings.WP_ALLOWED_IPS = ['127.0.0.1']

    def test_without_token(self):
        # Create an instance of a GET request for creating auth_token.
        request = self.factory.get('/')

        auth_data = SuperAdminAuthentication().authenticate(request)

        assert auth_data is None

    def test_empty_token(self):
        # Generate Authorization header to create request for authentication.
        authorization_header = "Token {token}".format(token='')

        # Create an instance of a GET request for validating auth_token.
        auth_request = self.factory.get('/', HTTP_AUTHORIZATION=authorization_header)

        # Authenticate auth request
        with pytest.raises(AuthenticationFailed):
            SuperAdminAuthentication().authenticate(auth_request)

    def test_invalid_token(self):
        # Generate Authorization header to create request for authentication.
        authorization_header = "Token {token}".format(token='invalid-test-token')

        # Create an instance of a GET request for validating auth_token.
        auth_request = self.factory.get('/', HTTP_AUTHORIZATION=authorization_header)

        # Authenticate auth request
        with pytest.raises(AuthenticationFailed):
            SuperAdminAuthentication().authenticate(auth_request)

    def test_valid_superadmin_token(self):
        # Generate Authorization header to create request for authentication.
        authorization_header = "Token {token}".format(token='2m#pi1x)175ekzji-&*3s^a$1l=*xo06$4#)bdj4%!dqp-)*mu')

        # Create an instance of a GET request for validating auth_token.
        auth_request = self.factory.get('/', HTTP_AUTHORIZATION=authorization_header)

        # Authenticate auth request
        auth_data = SuperAdminAuthentication().authenticate(auth_request)

        assert auth_data[0].is_superuser

    def test_invalid_ip(self):
        settings.WP_ALLOWED_IPS = ['127.0.0.2']
        # Generate Authorization header to create request for authentication.
        authorization_header = "Token {token}".format(token='2m#pi1x)175ekzji-&*3s^a$1l=*xo06$4#)bdj4%!dqp-)*mu')

        # Create an instance of a GET request for validating auth_token.
        auth_request = self.factory.get('/', HTTP_AUTHORIZATION=authorization_header)

        # Authenticate auth request
        with pytest.raises(AuthenticationFailed):
            SuperAdminAuthentication().authenticate(auth_request)
