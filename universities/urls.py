from django.urls import path
from .views import ProgramListAPIView, UniversityListAPIView, IntakeListAPIView


urlpatterns = [
    path('uni_list/', UniversityListAPIView.as_view(), name='uni-list'),
    path('programs/<int:university_id>/', ProgramListAPIView.as_view(), name='program-list'),
    path('intakes/<int:program_id>/', IntakeListAPIView.as_view(), name='IntakeList')
]
