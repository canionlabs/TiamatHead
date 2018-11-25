from django.urls import path

from apps.projects.views import ProjectListCreateView, ProjectDetailView


app_name = 'projects'

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='list-create-projects'),
    path('projects/<pk>/', ProjectDetailView.as_view(), name='detail-projects')
]
