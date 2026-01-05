from django.urls import path
from .views import ProfileRetrieveAPIView, ProfileFollowAPIView

urlpatterns = [
    path('profiles/<str:username>/', ProfileRetrieveAPIView.as_view(), name='profile'),
    path('profiles/<str:username>/follow/', ProfileFollowAPIView.as_view(), name='profile-follow'),
]
