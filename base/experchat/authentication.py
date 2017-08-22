from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication, exceptions


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        User = get_user_model()

        try:
            auth_data = signing.loads(token, key=settings.AUTH_SIGNING_KEY)
        except signing.BadSignature:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        try:
            user = User.objects.get(id=auth_data.get('user_id', None))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # Get user type from request url
        if request.resolver_match is None:
            user_type = ''
        else:
            user_type = request.resolver_match.kwargs.get('user_type', '')

        if user_type in ['expert', 'user']:
            # Allow expert to only expert-urls and user to user-urls.
            if hasattr(user, user_type):
                return (user, None)
            elif user.is_superuser:  # Allow superusers to all URLs.
                return (user, None)
            else:
                raise exceptions.AuthenticationFailed(_('Invalid token.'))
        else:
            return (user, None)

    def authenticate_header(self, request):
        return self.keyword

    @classmethod
    def generate_credentials(cls, request, user_id):
        """
        Generate authentication token using django signing and AUTH_SIGNING_KEY.
        """
        ip_address = (request.META.get('HTTP_X_FORWARDED_FOR', '') or
                      request.META.get('REMOTE_ADDR'))
        auth_data = {
            "user_id": user_id,
            "timestamp": timezone.datetime.timestamp(timezone.now()),
            "ip_address": ip_address,
        }
        return signing.dumps(auth_data, key=settings.AUTH_SIGNING_KEY)


class SuperAdminAuthentication(authentication.BaseAuthentication):
    """
    Fix token from environment based authentication for wordpress.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')

        if ip_address not in getattr(settings, 'WP_ALLOWED_IPS', ['127.0.0.1']):
            raise exceptions.AuthenticationFailed(_('This IP Address is not allowed.'))

        if hasattr(settings, 'WP_SUPER_ADMIN_TOKEN') and token == settings.WP_SUPER_ADMIN_TOKEN:
            User = get_user_model()
            user = User(is_superuser=True, is_staff=True, is_email_verified=True)
            return (user, None)

        raise exceptions.AuthenticationFailed(_('Invalid token.'))

    def authenticate_header(self, request):
        return self.keyword
