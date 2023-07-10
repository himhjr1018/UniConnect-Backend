"""
URL configuration for uniConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


urlpatterns = [
    path('admin/', admin.site.urls),
    path('universities/', include('universities.urls')),
    path('user/', include('users.urls')),
    path('ms_graph/', include('microsoft_graph.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="UniConnect API",
        default_version='v1',
        description="UniConnect REST API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=OpenAPISchemaGenerator
)
urlpatterns.append(path('api_doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))