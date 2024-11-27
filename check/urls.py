from . import views
from django.urls import pathlib


urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
]