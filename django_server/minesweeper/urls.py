from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', obtain_jwt_token),
    path('api/refresh/', refresh_jwt_token),
    path('', include('homepage.urls')),
    path('join/', include('homepage.urls')),
    path('game/', include('homepage.urls')),
]

