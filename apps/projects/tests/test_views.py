from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from model_mommy import mommy

from apps.common.utils._tests import BaseTest, UserModel, \
    AccessToken, Application

import pytest
import datetime


BASE_QUANTITY = 10


@pytest.fixture(scope='class')
def oauth_user(request):
    user = UserModel.objects.create_user(
        username=request.instance.random_string(),
        email=request.instance.random_email(),
        password=request.instance.random_string()
    )

    non_user = UserModel.objects.create_user(
        username=request.instance.random_string(),
        email=request.instance.random_email(),
        password=request.instance.random_string()
    )

    request.cls.user = user
    request.cls.non_user = non_user


@pytest.mark.usefixtures('oauth_user')
class ProjectViewSetTests(APITestCase, BaseTest):
    def setUp(self):
        self.organization = mommy.make(
            'auth_management.Organization', make_m2m=True
        )

        self.organization.users.add(self.user)
        self.projects = mommy.make(
            'projects.Project', organization=self.organization,
            _quantity=BASE_QUANTITY
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.organization.delete()

    def test_list_projects(self):
        url = reverse('projects:project-list')
        response = self.client.get(url)
        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(content) == BASE_QUANTITY

    def test_list_projects_without_organization(self):
        self.client.force_authenticate(user=self.non_user)

        url = reverse('projects:project-list')
        response = self.client.get(url)
        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(content) == 0


# @pytest.fixture(scope='class')
# def class_projects(request):
#     serialized_project = {'name': request.instance.random_string()}
#     request.cls.serialized_project = serialized_project


# @pytest.mark.usefixtures('class_projects')
# class ProjectListTest(BaseDefaultTest):
#     """
#     Testing GET 'projects:list-create-projects'
#     """
#     def setUp(self):
#         super(ProjectListTest, self).setUp()
#         self.serialized_project.update({'organization': self.organization})
#         self.new_project = Project.objects.create(**self.serialized_project)
#         self.new_project.members.add(self.test_user)

#         self.non_project_user = UserModel.objects.create_user(
#             username=self.random_string(),
#             email=self.random_email(), password=str(self.uuid4())
#         )
#         self.np_user_token = AccessToken.objects.create(
#             user=self.non_project_user, token=str(self.uuid4()),
#             application=self.application,
#             expires=timezone.now() + datetime.timedelta(days=1),
#             scope="read write dolphin"
#         )
#         self.np_user_headers = {
#             "HTTP_AUTHORIZATION": f"Bearer {self.np_user_token.token}",
#         }

#     def tearDown(self):
#         self.new_project.delete()

#     def test_list_projects(self):
#         response = self.client.get(
#             reverse('projects:list-create-projects'),
#             **self.auth_user_headers
#         )
#         self.assertEqual(status.HTTP_200_OK, response.status_code)

#         data = response.json()
#         projects_count = self.test_user.projects.all().count()
#         self.assertEqual(projects_count, len(data))

#     def test_list_projects_without_user(self):
#         response = self.client.get(
#             reverse('projects:list-create-projects'),
#             **self.np_user_headers
#         )
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(response.json(), [])

#     def test_list_filtering_projects(self):
#         url_reverse = self.custom_reverse(
#             'projects:list-create-projects',
#             query_kwargs={'project_id': self.new_project.id}
#         )
#         response = self.client.get(url_reverse, **self.auth_user_headers)

#         projects_count = Project.objects.filter(id=self.new_project.id).count()
#         data = response.json()
#         self.assertEqual(projects_count, len(data))


# @pytest.mark.usefixtures('class_projects')
# class ProjectCreateTest(BaseDefaultTest):
#     """
#     Testing POST 'projects:list-create-projects'
#     """
#     def setUp(self):
#         super(ProjectCreateTest, self).setUp()

#         # user without organization
#         self.norg_user = UserModel.objects.create_user(
#             username=self.random_string(),
#             email=self.random_email(), password=self.uuid4()
#         )
#         self.norg_user_token = AccessToken.objects.create(
#             user=self.norg_user, token=str(self.uuid4()),
#             application=self.application,
#             expires=timezone.now() + datetime.timedelta(days=1),
#             scope="read write dolphin"
#         )
#         self.norg_user_headers = {
#             "HTTP_AUTHORIZATION": f"Bearer {self.norg_user_token.token}",
#         }

#     def tearDown(self):
#         self.norg_user.delete()
#         self.norg_user_token.delete()

#     def test_create_project(self):
#         to_send = self.serialized_project
#         to_send.update(organization_id=str(self.organization.id))

#         response = self.client.post(
#             reverse('projects:list-create-projects'),
#             **self.auth_user_headers,
#             data=to_send
#         )

#         self.assertEqual(status.HTTP_201_CREATED, response.status_code)
#         res = response.json()
#         for field, value in res.items():
#             sent_value = to_send.get(field)
#             if sent_value:
#                 self.assertEqual(value, str(sent_value))

#     def test_create_project_with_invalid_organization(self):
#         to_send = self.serialized_project
#         to_send.update(organization_id=str(self.uuid4()))

#         response = self.client.post(
#             reverse('projects:list-create-projects'),
#             **self.auth_user_headers,
#             data=to_send
#         )
#         self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

#     def test_create_project_with_no_related_user(self):
#         to_send = self.serialized_project
#         to_send.update(organization_id=str(self.uuid4()))

#         response = self.client.post(
#             reverse('projects:list-create-projects'),
#             **self.auth_user_headers,
#             data=to_send
#         )
#         self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


# @pytest.mark.usefixtures('class_projects')
# class ProjectRetrieveTest(BaseDefaultTest):
#     """
#     Testing GET 'projects:detail-project'
#     """
#     def setUp(self):
#         super(ProjectRetrieveTest, self).setUp()
#         self.serialized_project.update({'organization': self.organization})
#         self.new_project = Project.objects.create(**self.serialized_project)

#     def tearDown(self):
#         self.new_project.delete()

#     def test_retrieve_project(self):
#         response = self.client.get(
#             reverse(
#                 'projects:detail-projects',
#                 kwargs={'pk': self.project.project_id}
#             ),
#             **self.auth_user_headers
#         )
#         self.assertEqual(status.HTTP_200_OK, response.status_code)

#         content = response.json()
#         serialize_project = ProjectSerializer(instance=self.project).data

#         self.assertDictEqual(serialize_project, content)
#         for content_key, content_value in content.items():
#             self.assertEqual(serialize_project.get(content_key), content_value)

#     def test_retrive_no_related_project(self):
#         response = self.client.get(
#             reverse(
#                 'projects:detail-projects',
#                 kwargs={'pk': self.new_project.project_id}
#             ),
#             **self.auth_user_headers
#         )
#         self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


# class ProjectUpdateTest(BaseDefaultTest):
#     """
#     Testing PATCH 'projects:detail-projects'
#     """
#     def test_update_name_project(self):
#         to_send = {'name': self.random_string()}

#         response = self.client.patch(
#             reverse(
#                 'projects:detail-projects',
#                 kwargs={'pk': self.project.project_id}
#             ),
#             data=to_send,
#             **self.auth_user_headers
#         )

#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         content = response.json()
#         for sent_key, sent_value in to_send.items():
#             self.assertEqual(content.get(sent_key), sent_value)

#     def test_update_project_id_read_only(self):
#         to_send = {'project_id': self.uuid4()}

#         response = self.client.patch(
#             reverse(
#                 'projects:detail-projects',
#                 kwargs={'pk': self.project.project_id}
#             ),
#             data=to_send,
#             **self.auth_user_headers
#         )

#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         content = response.json()

#         for sent_key, sent_value in to_send.items():
#             self.assertNotEqual(content.get(sent_key), sent_value)


# class ProjectDestroyTest(BaseDefaultTest):
#     """
#     Testing DELETE 'projects:detail-projects'
#     """
#     def setUp(self):
#         super(ProjectDestroyTest, self).setUp()
#         self.new_organization = Organization.objects.create(
#             name=self.random_string()
#         )
#         self.new_project = Project.objects.create(
#             name=self.random_string(),
#             organization=self.new_organization
#         )

#     def tearDown(self):
#         self.new_organization.delete()
#         self.new_project.delete()

#     def test_delete_project(self):
#         response = self.client.delete(
#             reverse(
#                 'projects:detail-projects',
#                 kwargs={'pk': self.project.project_id}
#             ),
#             **self.auth_user_headers
#         )
#         self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

#     def test_delete_project_with_permission(self):
#         response = self.client.delete(
#             reverse(
#                 'projects:detail-projects',
#                 kwargs={'pk': self.new_project.project_id}
#             ),
#             **self.auth_user_headers
#         )
#         self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
