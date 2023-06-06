from django.contrib import admin
from users.models import UserProfile, CustomToken

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomToken)
