from django.urls import path
from .views import ProgramListAPIView, UniversityListAPIView, IntakeListAPIView, CountryListView, UniversityListView, \
    UniversityCreateView


urlpatterns = [
    path('uni_list', UniversityListAPIView.as_view(), name='uni-list'),
    path('programs/<int:university_id>/', ProgramListAPIView.as_view(), name='program-list'),
    path('intakes/<int:program_id>/', IntakeListAPIView.as_view(), name='IntakeList'),
    path('countries/', CountryListView.as_view(), name="country_list"),
    path('add/', UniversityCreateView.as_view(), name="add_university"),
    path('', UniversityListView.as_view(), name="universities")
]
