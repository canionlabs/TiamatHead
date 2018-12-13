from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.auth_management.models import Organization
from apps.common.utils._tests import BaseDefaultTest, AccessToken, UserModel

import pytest

import datetime


class TestUserManagementView(BaseDefaultTest):
    """
    Testing POST 'projects:list-create-projects'
    """
    def setUp(self):
        super(TestUserManagementView, self).setUp()
        self.adm_urls = ['list-users', 'detail-users', 'list-groups']
        self.test_group = Group.objects.create(name=self.random_string())
        self.test_superuser = UserModel.objects.create_superuser(
            username=self.random_string(),
            email=self.random_email(), password=self.uuid4()
        )
        self.valid_admin_token = AccessToken.objects.create(
            user=self.test_superuser, token=self.uuid4(),
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )
        self.auth_admin_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.valid_admin_token.token}",
        }

    def tearDown(self):
        super(TestUserManagementView, self).tearDown()
        self.test_group.delete()
        self.test_superuser.delete()
        self.valid_admin_token.delete()

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


@pytest.fixture(scope='class')
def class_organizations(request):
    serialized_organization = {'name': request.instance.random_string()}
    request.cls.serialized_organization = serialized_organization


@pytest.mark.usefixtures('class_organizations')
class OrganizationListCreateTest(BaseDefaultTest):
    """
    Testing POST/GET in 'auth_management:list-create-organizations'
    """
    def setUp(self):
        super(OrganizationListCreateTest, self).setUp()
        self.test_superuser = UserModel.objects.create_superuser(
            username=self.random_string(),
            email=self.random_email(), password=self.uuid4()
        )
        self.valid_admin_token = AccessToken.objects.create(
            user=self.test_superuser, token=self.uuid4(),
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )
        self.auth_admin_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.valid_admin_token.token}",
        }

    def tearDown(self):
        super(OrganizationListCreateTest, self).tearDown()
        self.test_superuser.delete()
        self.valid_admin_token.delete()

    def test_list_organizations(self):
        response = self.client.get(
            reverse(
                'auth_management:list-create-organizations'
            ),
            **self.auth_user_headers
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = response.json()
        self.assertEqual(len(content), self.test_user.organizations.all().count())


class OrganizationAddUsersTest(BaseDefaultTest):
    """
    Testing POST in 'auth_management:create-organization-users'
    """
    BASE_URL = 'auth_management:create-organization-users'

    def test_add_organization_users(self):
        to_send = {'users': [self.test_user.username]}
        response = self.client.post(
            reverse(
                self.BASE_URL, kwargs={'pk': self.organization.id}
            ),
            data=to_send,
            **self.auth_user_headers
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        content = response.json()
        self.assertDictEqual(content, to_send)


class OrganizationRemoveUsersTest(BaseDefaultTest):
    """
    Testing DELETE in 'auth_management:remove-organization-users'
    """
    BASE_URL = 'auth_management:remove-organization-users'

    def test_remove_organization_users(self):
        to_send = {'users': [self.test_user.username]}
        response = self.client.delete(
            reverse(
                self.BASE_URL, kwargs={'pk': self.organization.id}
            ),
            data=to_send,
            **self.auth_user_headers
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        content = response.json()
        self.assertDictEqual(content, to_send)

    # def test_list_organization_users(self):
    #     response = self.client.get(
    #         reverse(self.BASE_URL, kwargs={'pk': self.organization.id}),
    #         **self.auth_user_headers
    #     )
    #     import pdb; pdb.set_trace()
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)

    # def test_list_organizations_as_supersuper(self):
    #     response = self.client.get(
    #         reverse(
    #             'auth_management:list-create-organizations'
    #         ),
    #         **self.auth_user_headers
    #     )
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     content = response.json()
    #     self.assertEqual(len(content), self.org_query.count())
    #     for content_org in content:
    #         org_id = content_org.get('organization_id')
    #         self.assertTrue(self.org_query.filter(id=org_id).exists())

    # def test_create_organization(self):
    #     to_send = self.serialized_organization
    #     to_send.update(
    #         {'users': [{'username': self.test_user.username}]}
    #     )
    #     response = self.client.post(
    #         reverse(
    #             'auth_management:list-create-organizations'
    #         ),
    #         **self.auth_user_headers,
    #         data=to_send
    #     )

    #     import pdb; pdb.set_trace()
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
