from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

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
        self.test_group = Group.objects.create(
            name='Test Group'
        )

        self.test_superuser = UserModel.objects.create_superuser(
            username='admintest',
            email='admintest@test.ts', password='admsuper-@pass2s'
        )

        self.test_user = UserModel.objects.create_user(
            username='test',
            email='test@test.ts', password='super-@pass2s'
        )

        self.application = Application(
            name="Test Application",
            user=self.test_superuser,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        self.valid_admin_token = AccessToken.objects.create(
            user=self.test_superuser, token="12345678901",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )

        self.valid_user_token = AccessToken.objects.create(
            user=self.test_user, token="12345678902",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )

        self.auth_admin_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.valid_admin_token.token}",
        }

        self.auth_user_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.valid_user_token.token}",
        }

        self.adm_urls = ['list-users', 'detail-users', 'list-groups']
    
    def tearDown(self):
        self.test_superuser.delete()


class TestUserManagementView(BaseTest):

    def test_non_admin_users(self):
        for adm_url in self.adm_urls:
            if adm_url.startswith('detail'):
                response = self.client.get(
                    reverse(
                        f'auth_management:{adm_url}', 
                        kwargs={'pk': self.test_user.id}
                    ),
                    **self.auth_user_headers
                )
            else:
                response = self.client.get(
                    reverse(f'auth_management:{adm_url}'),
                    **self.auth_user_headers
                )
            self.assertEqual(response.status_code, 403)

    def test_group_list(self):
        response = self.client.get(
            reverse('auth_management:list-groups'),
            **self.auth_admin_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(len(content), Group.objects.all().count())

    def test_user_list(self):
        response = self.client.get(
            reverse('auth_management:list-users'),
            **self.auth_admin_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()

        self.assertEqual(len(content), UserModel.objects.all().count())

    def test_user_detail(self):
        response = self.client.get(
            reverse(
                'auth_management:detail-users',
                kwargs={'pk': self.test_superuser.id}
            ),
            **self.auth_admin_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()

        expected_response = {
            'username': self.test_superuser.username,
            'email': self.test_superuser.email,
            'first_name': self.test_superuser.first_name,
            'last_name': self.test_superuser.last_name
        }
        self.assertDictEqual(content, expected_response)

