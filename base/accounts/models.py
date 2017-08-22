"""
Provide model user and user-account related models.
"""
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


def get_username(*args, **kwargs):
    return str(uuid.uuid4().hex)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Store User account details.
    """
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        default=get_username,
    )
    email = models.EmailField(_('email address'), max_length=100, db_index=True)

    name = models.CharField(_('name'), validators=[MinLengthValidator(2)], max_length=100)
    profile_photo = models.URLField(_('profile photo'), null=True, blank=True)

    country_code = models.PositiveSmallIntegerField(default=1)
    phone_number = models.CharField(max_length=16)
    is_phone_number_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                   'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    modified_timestamp = models.DateTimeField(_('modified timestamp'), auto_now=True)
    toc_and_privacy_policy_accepted = models.BooleanField(
        _('terms & condition and privacy policy accepted'),
        default=False
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['name', 'email']   # Set it as required.

    def __str__(self):
        return '{name} <{email}>'.format(
            name=self.name,
            email=self.email,
        )

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @classmethod
    def signup(cls, email, password, username=None):
        """
        Signups user as unverified and sends email for verification.

        Args:
            email: email to signup with.
            password: password to be set for user.
            username: username to be used for user.

        Returns:
            user instance.
        """
        hashed_password = make_password(password)

        if username is None:
            username = get_username()

        instance = cls.objects.create(email=email, password=hashed_password, is_active=True, username=username,
                                      toc_and_privacy_policy_accepted=True)

        return instance
