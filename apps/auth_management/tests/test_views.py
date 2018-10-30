from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from oauth2_provider.models import get_access_token_model, get_application_model

import datetime


Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


class BaseTest(APITestCase):
    def setUp(self):
        self.test_user = UserModel.objects.create_user(
            username='test', email='test@test.ts', password='super-@pass2s'
        )

        self.application = Application(
            name="Test Application",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        self.valid_token = AccessToken.objects.create(
            user=self.test_user, token="12345678901",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )

        self.auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.valid_token.token,
        }

        self.application.save()
    
    def tearDown(self):
        self.test_user.delete()


class TestUserView(BaseTest):

    def test_user_list(self):
        response = self.client.get(
            reverse('auth_management:list-users'),
            **self.auth_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()

        self.assertEqual(len(content), 1)

    def test_user_detail(self):
        response = self.client.get(
            reverse(
                'auth_management:detail-users', 
                kwargs={'pk': self.test_user.id}
            ),
            **self.auth_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()

        expected_response = {
            'username': self.test_user.username,
            'email': self.test_user.email,
            'first_name': self.test_user.first_name,
            'last_name': self.test_user.last_name
        }
        self.assertDictEqual(content, expected_response)

