# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.urls import reverse

# from rest_framework.test import APITestCase

# from oauth2_provider.models import get_access_token_model, get_application_model

from apps.devices.models import Device
from apps.projects.models import Project
from apps.auth_management.models import Organization

# import datetime
# import uuid


# Application = get_application_model()
# AccessToken = get_access_token_model()
# UserModel = get_user_model()


# class BaseTest(APITestCase):
#     def setUp(self):
#         self.test_user = UserModel.objects.create_user(
#             username='test',
#             email='test@test.ts', password=str(uuid.uuid4())
#         )

#         self.application = Application(
#             name="Test Application",
#             user=self.test_user,
#             client_type=Application.CLIENT_CONFIDENTIAL,
#             authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
#         )
#         self.application.save()

#         self.valid_user_token = AccessToken.objects.create(
#             user=self.test_user, token=uuid.uuid4().hex,
#             application=self.application,
#             expires=timezone.now() + datetime.timedelta(days=1),
#             scope="read write dolphin"
#         )

#         self.auth_user_headers = {
#             "HTTP_AUTHORIZATION": f"Bearer {self.valid_user_token.token}",
#         }

#         self.test_device = Device.objects.create(
#             name='Test Device',
#             user=self.test_user
#         )

#         self.norelated_user = UserModel.objects.create_user(
#             username='test-norelated',
#             email='test@test.ts', password=str(uuid.uuid4())
#         )

#         self.valid_norelated_user_token = AccessToken.objects.create(
#             user=self.norelated_user, token=uuid.uuid4().hex,
#             application=self.application,
#             expires=timezone.now() + datetime.timedelta(days=1),
#             scope="read write dolphin"
#         )

#         self.auth_norelated_user_headers = {
#             "HTTP_AUTHORIZATION": f"Bearer {self.valid_norelated_user_token.token}",
#         }

#     def tearDown(self):
#         self.test_user.delete()
#         self.test_device.delete()
#         self.valid_user_token.delete()

from django.urls import reverse

from apps.common.utils._tests import BaseDefaultTest


class DeviceListTest(BaseDefaultTest):
    """
    Testing 'devices:list-devices'
    """

    def test_list_devices(self):
        response = self.client.get(
            reverse('devices:list-devices'),
            **self.auth_user_headers
        )
        self.assertEqual(response.status_code, 200)

        content = response.json()
        device_count = Device.objects.filter(
            project__organization__users=self.test_user
        ).count()
        self.assertEqual(len(content), device_count)

    def test_list_devices_filters(self):
        url_reverse = self.custom_reverse(
            'devices:list-devices',
            query_kwargs={'project_id': self.project.id}
        )
        response = self.client.get(url_reverse, **self.auth_user_headers)

        device_count = Device.objects.filter(
            project__organization__users=self.test_user
        ).count()

        content = response.json()
        self.assertEqual(len(content), device_count)
    
    def test_list_devices_filter_multiple_projects(self):
        new_project = Project.objects.create(
            creator=self.test_user,
            name='New Test Project',
            organization=self.organization
        )

        new_device = Device.objects.create(
            name='New Test Device',
            project=self.project
        )

        url_reverse = self.custom_reverse(
            'devices:list-devices',
            query_kwargs={'project_id': new_project.id}
        )

        response = self.client.get(url_reverse, **self.auth_user_headers)
        content = response.json()

        self.assertEqual(len(content), 0)
        new_project.delete()
        new_device.delete()

    def test_list_devices_filter_errors(self):
        self.organization.users.remove(self.test_user)

        url_reverse = self.custom_reverse(
            'devices:list-devices',
            query_kwargs={'project_id': self.project.id}
        )
        response = self.client.get(url_reverse, **self.auth_user_headers)

        content = response.json()
        self.assertEqual(len(content), 0)

        self.organization.users.add(self.test_user)


class DeviceCreateTest(BaseDefaultTest):
    pass


class DeviceRetrieveTest(BaseDefaultTest):

    def test_retrieve_device(self):
        response = self.client.get(
            reverse(
                'devices:detail-devices',
                kwargs={'pk': self.test_device.id}
            ),
            **self.auth_user_headers
        )
        self.assertEqual(response.status_code, 200)

        response_device_id = response.json().get('device_id')
        self.assertEqual(str(self.test_device.id), response_device_id)

    def test_retrieve_non_related_device(self):
        new_organization = Organization.objects.create(
            name='Organization'
        )
        new_project = Project.objects.create(
            creator=self.test_user,
            name='New Test Project',
            organization=new_organization
        )
        new_device = Device.objects.create(
            name='New Test Device',
            project=new_project
        )

        response = self.client.get(
            reverse(
                'devices:detail-devices',
                kwargs={'pk': new_device.id}
            ),
            **self.auth_user_headers
        )

        self.assertEqual(response.status_code, 403)

    # def test_detail_devices(self):
    #     response = self.client.get(
    #         reverse(
    #             'devices:detail-devices',
    #             kwargs={'pk': self.test_device.device_id}
    #         ),
    #         **self.auth_user_headers
    #     )
    #     self.assertEqual(response.status_code, 200)

    #     content = response.json()
    #     expected_response = {
    #         'name': self.test_device.name,
    #         'device_id': str(self.test_device.device_id),
    #         'user': {
    #             'username': self.test_device.user.username,
    #             'id': self.test_device.user.id
    #         }
    #     }
    #     self.assertDictEqual(content, expected_response)

    # def test_create_and_update_devices(self):
    #     # Create
    #     response = self.client.post(
    #         reverse('devices:list-devices'),
    #         **self.auth_user_headers,
    #         data={
    #             'name': 'test create device',
    #             'project': {
    #                 'organization': self.project.id
    #             }
    #         }
    #     )
    #     self.assertEqual(response.status_code, 201)

    #     content = response.json()
    #     self.assertEqual(
    #         response.data['name'], content['name']
    #     )

    #     # Update
    #     old_name = response.data['name']
    #     response = self.client.patch(
    #         reverse(
    #             'devices:detail-devices',
    #             kwargs={'pk': content['device_id']}
    #         ),
    #         **self.auth_user_headers,
    #         data={'name': 'new device'}
    #     )
    #     self.assertEqual(response.status_code, 200)

    #     content = response.json()
    #     self.assertNotEqual(old_name, content['name'])
    #     self.assertEqual(response.data['name'], content['name'])

    # def test_update_norelated_user(self):
    #     response = self.client.post(
    #         reverse('devices:list-devices'),
    #         **self.auth_user_headers,
    #         data={'name': 'test create device'}
    #     )
    #     self.assertEqual(response.status_code, 201)
    #     content = response.json()
    #     device_id = content['device_id']

    #     content = response.json()
    #     self.assertEqual(response.data['name'], content['name'])

    #     response = self.client.patch(
    #         reverse(
    #             'devices:detail-devices',
    #             kwargs={'pk': device_id}
    #         ),
    #         **self.auth_norelated_user_headers,
    #         data={'name': 'Invalid name'}
    #     )

    #     self.assertNotEqual(response.status_code, 200)
    
    # def test_delete_devices(self):
    #     test_device = Device.objects.create(
    #         user = self.test_user
    #     )
    #     response = self.client.delete(
    #         reverse(
    #             'devices:detail-devices',
    #             kwargs={'pk': test_device.device_id}
    #         ),
    #         **self.auth_user_headers,
    #     )
    #     self.assertEqual(response.status_code, 204)

    # def test_delete_norelated_user(self):
    #     test_device = Device.objects.create(
    #         user=self.test_user
    #     )
    #     response = self.client.delete(
    #         reverse(
    #             'devices:detail-devices',
    #             kwargs={'pk': test_device.device_id}
    #         ),
    #         **self.auth_norelated_user_headers,
    #     )

    #     self.assertEqual(response.status_code, 403)
