"""tiamat_head URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
admin.autodiscover()


schema_view = get_schema_view(
   openapi.Info(
      title="Timat API",
      default_version='v1',
      description="Gateway between end applications and Tiamat services",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="caio@canionlabs.io"),
      license=openapi.License(name="MIT License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('apps.auth_management.urls', namespace='auth_management')),
    path('', include('apps.devices.urls', namespace='devices'))
]
