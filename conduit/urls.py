"""
URL configuration for conduit project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('profiles.urls')),
    path('api/', include('articles.urls')),
    path('', include('frontend.urls')),
]
