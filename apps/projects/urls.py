from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectViewSet


app_name = 'projects'
router = DefaultRouter()
router.register('projects', ProjectViewSet, 'project')

urlpatterns = router.urls
