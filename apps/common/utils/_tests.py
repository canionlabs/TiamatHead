from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from django.utils import timezone
from django.urls import reverse

from rest_framework.test import APITestCase
from oauth2_provider.models import get_access_token_model, get_application_model

from apps.devices.models import Device
from apps.projects.models import Project
from apps.auth_management.models import Organization

import uuid
import random
import string
import datetime


Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


class BaseTest():

    def __init__(self):
        pass

    def custom_reverse(self, view_name, kwargs=None, query_kwargs=None):
        """
        Create an reverse url using query params
        """
        url = reverse(view_name, kwargs=kwargs)

        if query_kwargs:
            return f'{url}?{urlencode(query_kwargs)}'  
        return url
    
    def random_string(self):
        return ''.join(
            [random.choice(string.ascii_letters) for n in range(12)]
        )
    
    def random_email(self):
        return (
            f'{self.random_string}@{self.random_string}.{self.random_string}'
        )
    
    def uuid4(self):
        return uuid.uuid4()


class BaseDefaultTest(APITestCase, BaseTest):

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

        self.organization = Organization.objects.create(
            name='Test Organization'
        )
        self.organization.users.add(self.test_user)

        self.project = Project.objects.create(
            name='Test Project',
            organization=self.organization
        )
        self.project.members.add(self.test_user)

        self.test_device = Device.objects.create(
            name='Test Device',
            project=self.project
        )

    def tearDown(self):
        self.test_user.delete()
        self.application.delete()
        self.test_device.delete()
        self.valid_user_token.delete()
        self.organization.delete()
        self.project.delete()
