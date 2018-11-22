from rest_framework.test import APITestCase

from rest_framework import status

from apps.common.utils._tests import BaseTest, UserModel
from apps.projects.models import Project
from apps.auth_management.models import Organization

import uuid


class ProjectModelTest(APITestCase, BaseTest):
    """
    Testing the model projects.models.Project
    """
    def setUp(self):
        self.organization = Organization.objects.create(
            name=self.random_string()
        )

        self.project = Project.objects.create(
            name = self.random_string(),
            organization=self.organization
        )

        self.test_user = UserModel.objects.create_user(
            username=self.random_string(),
            email=self.random_email(), password=str(uuid.uuid4())
        )

    def tearDown(self):
        self.test_user.delete()
        self.project.delete()

    def test_related_query_with_users(self):
        self.project.members.add(self.test_user)
        project_query = self.test_user.projects.filter(
            id=self.project.project_id
        ).first()

        self.assertEqual(project_query, self.project)
