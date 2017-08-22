from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from devices.models import Device
from experchat.enumerations import DeviceStatus
from publisher.utils import ExperchatPublisher

User = get_user_model()


@pytest.mark.django_db
class TestDevices(TestCase):

    @mock.patch.object(ExperchatPublisher, 'add_push_device')
    def setUp(self, mock_add_push_device):
        mock_add_push_device.return_value = True

        self.user = User.objects.create(
            email="testuser@example.com",
            is_email_verified=True
        )
        self.device = Device.objects.create(
            user=User.objects.get(email='testuser@example.com'),
            device_id='device_id',
            device_token='device_token'
        )

    @mock.patch.object(ExperchatPublisher, 'remove_push_device')
    def test_device_soft_delete(self, mock_remove_push_device):
        mock_remove_push_device.return_value = None

        d_id = self.device.id
        self.device.delete()

        assert Device.objects.filter(id=d_id).exists() and self.device.status == DeviceStatus.INACTIVE.value
