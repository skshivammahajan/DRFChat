from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from registration.models import VerificationToken
from registration.utils import check_verify_notification_spamming


class TestNotificationSpamming(TestCase):

    def setUp(self):
        self.user = MagicMock()
        self.verificationtoken = MagicMock(spec=VerificationToken,
                                           user=self.user,
                                           purpose=1,
                                           notify_count=4)

    @mock.patch.object(VerificationToken, 'objects')
    def test_check_verify_notification_spamming_with_no_obj(self, mock_user_model):
        """
        Passing No object.
        """
        mock_user_model.filter.return_value.first.return_value = None
        result = check_verify_notification_spamming(self.user, 1)
        assert result is False

    @mock.patch.object(VerificationToken, 'objects')
    def test_check_verify_notification_spamming_False(self, mock_user_model):
        """
        Passing the object with under limit.
        """
        mock_user_model.filter.return_value.first.return_value = self.verificationtoken
        result = check_verify_notification_spamming(self.user, 1)
        assert result is False

    @mock.patch.object(VerificationToken, 'objects')
    def test_check_verify_notification_spamming_True(self, mock_user_model):
        """
        Passing the object with over limit.
        """
        self.verificationtoken.notify_count = 7
        mock_user_model.filter.return_value.first.return_value = self.verificationtoken
        result = check_verify_notification_spamming(self.user, 1)
        assert result is True
