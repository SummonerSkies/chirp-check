from . import views
from django.urls import path

urlpatterns = [
    """
    urls for the web app site
    """
    path("", views.HomePage.as_view(), name="home"),

    """
    chirp check checklist
    """

    """
    sign up
    """
]