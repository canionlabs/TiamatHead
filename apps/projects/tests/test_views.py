from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from apps.common.utils._tests import BaseDefaultTest, UserModel, AccessToken
from apps.projects.models import Project

import pytest
import datetime


@pytest.fixture(scope='class')
def class_projects(request):
    serialized_project = {'name': request.instance.random_string()}
    request.cls.serialized_project = serialized_project


@pytest.mark.usefixtures('class_projects')
class ProjectListTest(BaseDefaultTest):
    """
    Testing GET 'projects:list-create-projects'
    """
    def setUp(self):
        super(ProjectListTest, self).setUp()
        self.serialized_project.update({'organization': self.organization})
        self.new_project = Project.objects.create(**self.serialized_project)
        self.new_project.members.add(self.test_user)

        self.non_project_user = UserModel.objects.create_user(
            username=self.random_string(),
            email=self.random_email(), password=str(self.uuid4())
        )
        self.np_user_token = AccessToken.objects.create(
            user=self.non_project_user, token=str(self.uuid4()),
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin"
        )
        self.np_user_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.np_user_token.token}",
        }

    def tearDown(self):
        self.new_project.delete()

    def test_list_projects(self):
        response = self.client.get(
            reverse('projects:list-create-projects'),
            **self.auth_user_headers
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()
        projects_count = self.test_user.projects.all().count()
        self.assertEqual(projects_count, len(data))

    def test_list_projects_without_user(self):
        response = self.client.get(
            reverse('projects:list-create-projects'),
            **self.np_user_headers
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), [])

    def test_list_filtering_projects(self):
        pass
        # url_reverse = self.custom_reverse(
        #     'projects:list-create-projects',
        #     query_kwargs={'project_id': self.project.id}
        # )
        # response = self.client.get(url_reverse, **self.auth_user_headers)

        # projects_count = Project.objects.filter(id=self.project.id).count()
        # data = response.json()

        # self.assertEqual(projects_count, len(data))


# url_reverse = self.custom_reverse('projects:list-create-projects',query_kwargs={'project_id': self.project.id})