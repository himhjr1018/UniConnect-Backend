from django.urls import path
from users.views import LoginView, LogoutView, SignUpView, AddEducation, AddExperience, InterestedProgramCreateAPIView,\
    EducationUpdateAPIView, ExperienceUpdateAPIView, InterestedProgramUpdateAPIView, EducationDeleteAPIView, ExperienceDeleteAPIView,\
    InterestedProgramDeleteAPIView, ProfilePictureUploadAPIView, EditIntroAPIView, UsernameUpdateAPIView, UserDeleteAPIView, UserProfileDetailAPIView,\
    OUserProfileDetailAPIView, UserProfileListAPIView, InterestedProgramAPIView, InterestedProgramView




urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('add_edu/', AddEducation.as_view(), name='add_education'),
    path('add_exp/', AddExperience.as_view(), name='add_experience'),
    path('add_int_prog/', InterestedProgramCreateAPIView.as_view(), name='add_interested_program'),
    path('edit_edu/<int:id>/', EducationUpdateAPIView.as_view(), name='edit_education'),
    path('edit_exp/<int:id>/', ExperienceUpdateAPIView.as_view(), name='edit_experience'),
    path('edit_int_prog/<int:id>/', InterestedProgramUpdateAPIView.as_view(), name='edit_interested_program'),
    path('del_edu/<int:id>/', EducationDeleteAPIView.as_view(), name='delete_education'),
    path('del_exp/<int:id>/', ExperienceDeleteAPIView.as_view(), name='delete_experience'),
    path('del_int_prog/<int:id>/', InterestedProgramDeleteAPIView.as_view(), name='delete_interested_programs'),
    path('upload_pic/', ProfilePictureUploadAPIView.as_view(), name='upload_profile_pic'),
    path('edit_intro/', EditIntroAPIView.as_view(), name='edit_intro'),
    path('update_username/', UsernameUpdateAPIView.as_view(), name='update_username'),
    path('remove_user/', UserDeleteAPIView.as_view(), name='remove_user'),
    path('profile/', UserProfileDetailAPIView.as_view(), name='profile_detail'),
    path('<int:id>/profile/', OUserProfileDetailAPIView.as_view(), name='oprofile_detail'),
    path('profile_list/', UserProfileListAPIView.as_view(), name="profile_list"),
    path('<int:user_id>/favourites/', InterestedProgramAPIView.as_view(), name="ip_list"),
    path('add_favourite/', InterestedProgramView.as_view(), name="add_favourite")
]
