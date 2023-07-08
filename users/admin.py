from django.contrib import admin
from users.models import UserProfile, CustomToken, Education, Experience, InterestedProgram

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomToken)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(InterestedProgram)
