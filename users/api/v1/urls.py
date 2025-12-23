from django.urls import path
from .views import register_user, get_user

urlpatterns = [
    path('users/register/', register_user, name='user-register'),
    path('users/<int:user_id>/', get_user, name='user-profile'),
]