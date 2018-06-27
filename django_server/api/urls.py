from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('game/<int:pk>/', views.GameDetail.as_view()),
    path('games/', views.GameList.as_view(), name='games'),
    path('user/<str:username>/', views.UserDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('registration/', views.RegistrationAndObtainToken.as_view()),
    path('checkAuthorization/', views.CheckAuthorization.as_view()),
    path('login/', views.LoginAndObtainToken.as_view()),
    path('logout/', views.LogoutUser.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)