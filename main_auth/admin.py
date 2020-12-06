from django.contrib import admin


# Register your models here.
from main_auth.models import UserProfile

admin.site.register(UserProfile)
