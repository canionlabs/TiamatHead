from apps.common.utils._tests import BaseDefaultTest
from django.urls import reverse
from rest_framework import status


class ProjectListTest(BaseDefaultTest):
    """
    Testing GET 'projects:list-create-projects'
    """
    def test_list_projects(self):
        response = self.client.get(
            reverse('projects:list-create-projects'),
            **self.auth_user_headers
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()
        projects_count = self.test_user.projects.all().count()
        self.assertEqual(projects_count, len(data))

    def test_list_projects_without_project(self):
        self.project.members.remove(self.test_user)
        
        response = self.client.get(
            reverse('projects:list-create-projects'),
            **self.auth_user_headers
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()
        projects_count = self.test_user.projects.all().count()
        self.assertEqual(projects_count, len(data))
