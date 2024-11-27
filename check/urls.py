from . import viewsfrom django.urls import pathlib
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
]