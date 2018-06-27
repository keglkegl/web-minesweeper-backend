from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('<str:str>', views.homepageText),
]