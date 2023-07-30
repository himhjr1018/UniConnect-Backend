from django.urls import path
from .views import Community


urlpatterns = [
    path('<int:university_id>/', Community.as_view(), name='community'),
]
