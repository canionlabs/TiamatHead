from django.urls import path

from apps.projects.views import ProjectListCreateView


app_name = 'projects'

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='list-create-projects')
]
