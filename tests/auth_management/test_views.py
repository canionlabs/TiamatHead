from django.urls import reverse
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status
from model_mommy import mommy

from apps.common.utils.base_tests import BaseTest

import pytest
import random
from functools import reduce


@pytest.mark.usefixtures('oauth_user')
class OrganizationViewSetTest(APITestCase, BaseTest):

    BASE_QUANTITY = 4

    def setUp(self):
        self.random_users = mommy.make(
            settings.AUTH_USER_MODEL,
            _quantity=self.BASE_QUANTITY
        )
        self.empty_organizations = mommy.make(
            'auth_management.Organization',
            _quantity=self.BASE_QUANTITY, make_m2m=True
        )
        self.organizations = mommy.make(
            'auth_management.Organization',
            _quantity=self.BASE_QUANTITY, make_m2m=True
        )
        for orgs in self.organizations:
            orgs.users.add(self.user)

    def tearDown(self):
        pass

    def test_list_organizations(self):
        """
        GET user 'auth_management:organization-list'
        """
        url = reverse('auth_management:organization-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.user_header)
        response.status_code == status.HTTP_200_OK

        content = response.json()
        assert len(content) == self.BASE_QUANTITY

        for received_org in content:
            assert [
                org
                for org in self.organizations
                if str(org.id) == received_org.get('organization_id')
            ]

    def test_list_filtering_organizations(self):
        """
        GET user 'auth_management:organization-list'
        """
        selected_org = random.choice(self.organizations)
        available_filters = {
            'organization_id': selected_org.organization_id,
            'name': selected_org.name
        }

        for key_filter, value_filter in available_filters.items():
            url = self.custom_reverse(
                'auth_management:organization-list',
                query_kwargs={key_filter: value_filter}
            )
            response = self.client.get(
                url, HTTP_AUTHORIZATION=self.user_header
            )
            assert response.status_code == status.HTTP_200_OK

            content = response.json()
            for org in content:
                assert org.get('name') == selected_org.name
                assert (
                    org.get('organization_id') ==
                    str(selected_org.organization_id)
                )

    def test_list_filtering_nonexistent_organizations(self):
        """
        GET user 'auth_management:organization-list'
        """
        available_filters = {
            'organization_id': self.uuid4(),
            'name': self.random_string()
        }

        for key_filter, value_filter in available_filters.items():
            url = self.custom_reverse(
                'auth_management:organization-list',
                query_kwargs={key_filter: value_filter}
            )
            response = self.client.get(
                url, HTTP_AUTHORIZATION=self.user_header
            )
            assert response.status_code == status.HTTP_200_OK

            content = response.json()
            assert len(content) == 0

    def test_list_organizations_without_membership(self):
        """
        GET non_user 'auth_management:organization-list'
        """
        url = reverse('auth_management:organization-list')
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.non_user_header
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_create_organization(self):
        """
        POST user 'auth_management:organization-list'
        """
        to_send = {
            "name": self.random_string()
        }
        url = reverse('auth_management:organization-list')
        response = self.client.post(
            url, data=to_send, HTTP_AUTHORIZATION=self.user_header
        )

        assert response.status_code == status.HTTP_201_CREATED

        content = response.json()
        assert to_send['name'] in content.values()

        for user in content.get('users'):
            assert self.user.username in user.values()

    def test_create_organization_with_multiple_users(self):
        to_send = {
            "name": self.random_string(),
            "users": [user.username for user in self.random_users]
        }

        url = reverse('auth_management:organization-list')
        response = self.client.post(
            url, data=to_send, HTTP_AUTHORIZATION=self.user_header
        )

        assert response.status_code == status.HTTP_201_CREATED

        content = response.json()
        assert to_send['name'] in content.values()

        for user in content.get('users'):
            assert (
                user.get('username') in to_send['users'] or
                user.get('username') == self.user.username
            )
