from apps.devices.models import Device
from apps.projects.models import Project
from apps.auth_management.models import Organization

from django.urls import reverse

from apps.common.utils._tests import BaseDefaultTest

import pytest

import random
import string


@pytest.fixture(scope='class')
def class_devices(request):
    serialized_device = {
        'name': ''.join(
            [random.choice(string.ascii_letters) for n in range(12)]
        ),
        'project': ''
    }

    request.cls.serialized_device = serialized_device


class DeviceListTest(BaseDefaultTest):
    """
    Testing GET 'devices:list-create-devices'
    """
    def test_list_devices(self):
        response = self.client.get(
            reverse('devices:list-create-devices'),
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
            'devices:list-create-devices',
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
            name='New Test Project',
            organization=self.organization
        )

        new_device = Device.objects.create(
            name='New Test Device',
            project=self.project
        )

        url_reverse = self.custom_reverse(
            'devices:list-create-devices',
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
            'devices:list-create-devices',
            query_kwargs={'project_id': self.project.id}
        )
        response = self.client.get(url_reverse, **self.auth_user_headers)

        content = response.json()
        self.assertEqual(len(content), 0)

        self.organization.users.add(self.test_user)


@pytest.mark.usefixtures('class_devices')
class DeviceCreateTest(BaseDefaultTest):
    """
    Testing POST 'devices:list-create-devices'
    """
    def test_create_device_with_existent_project(self):
        """
        Creating a device using an existing project
        """
        to_send = self.serialized_device
        to_send.update(project=self.project.project_id)

        response = self.client.post(
            reverse('devices:list-create-devices'),
            **self.auth_user_headers,
            data=to_send
        )
        self.assertEqual(response.status_code, 201)
        
        res = response.json()
        for field, value in res.items():
            sent_value = to_send.get(field)
            if sent_value:
                self.assertEqual(value, str(sent_value))

    def test_create_device_without_project(self):
        """
        Trying force create a device without project
        """
        to_send = self.serialized_device

        response = self.client.post(
            reverse('devices:list-create-devices'),
            **self.auth_user_headers,
            data=to_send
        )
        self.assertEqual(response.status_code, 400)


class DeviceRetrieveTest(BaseDefaultTest):
    """
    Testing GET 'devices:detail-device'
    """
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


class DeviceUpdateTest(BaseDefaultTest):
    """
    Testing PATCH 'devices:detail-device'
    """
    def test_update_device(self):
        device_name = self.random_string()
        response = self.client.patch(
            reverse(
                'devices:detail-devices', 
                kwargs={'pk': self.test_device.id},
            ),
            data={
                'name': device_name
            },
            **self.auth_user_headers
        )

        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(data.get('name'), device_name)
    
    def test_update_device_without_credentials(self):
        response = self.client.patch(
            reverse(
                'devices:detail-devices',
                kwargs={'pk': self.random_string()}
            )
        )
        self.assertEqual(response.status_code, 401)


class DeviceDestroyTest(BaseDefaultTest):
    """
    Testing DELETE 'devices:detail-device'
    """
    def test_delete_device(self):
        response = self.client.delete(
            reverse(
                'devices:detail-devices',
                kwargs={'pk': self.test_device.id}
            ),
            **self.auth_user_headers
        )

        self.assertEqual(response.status_code, 204)
    
    def test_delete_device_without_permission(self):
        secondary_org = Organization.objects.create(
            name=self.random_string()
        )

        secondary_project = Project.objects.create(
            name=self.random_string(),
            organization=secondary_org
        )

        self.test_device.project = secondary_project
        self.test_device.save()

        response = self.client.delete(
            reverse(
                'devices:detail-devices',
                kwargs={'pk': self.test_device.id}
            ),
            **self.auth_user_headers
        )
        self.assertEqual(response.status_code, 403)
