from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase

from oauth2_provider.models import get_access_token_model, get_application_model

from apps.devices.models import Device

import datetime
import uuid


Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


class BaseTest(APITestCase):
    def setUp(self):
        self.test_user = UserModel.objects.create_user(
            username='test',
            email='test@test.ts', password=str(uuid.uuid4())
        )

        self.application = Application(
            name="Test Application",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        self.valid_user_token = AccessToken.objects.create(
            user=self.test_user, token=uuid.uuid4().hex,
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )

        self.auth_user_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.valid_user_token.token}",
        }

        self.test_device = Device.objects.create(
            name='Test Device',
            user=self.test_user
        )

    def tearDown(self):
        self.test_user.delete()
        self.test_device.delete()
        self.valid_user_token.delete()


class DeviceModelTest(BaseTest):
    def test_should_create_device(self):
        self.assertIsNotNone(self.test_device)

    def test_should_assert_methods(self):
        self.assertEqual(str(self.test_device), str(self.test_device.device_id))