from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserProfile

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('user', 'bio', 'image')
    search_fields = ('user__username', 'user__email')
