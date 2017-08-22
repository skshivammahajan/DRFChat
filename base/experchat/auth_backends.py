from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password


class EcEmailBackend(ModelBackend):
    """
    Support authentication using email and password based on user-type.
    """

    def authenticate(self, email="", password="", user_type=None, **kwargs):
        if user_type is None:
            return None

        if user_type not in ['expert', 'user']:
            return None

        try:
            user = get_user_model().objects.get(email__iexact=email, **{'%s__isnull' % user_type: False})
            if check_password(password, user.password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None
