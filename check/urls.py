from . import views
from django.urls import path

urlpatterns = [
    path("", views.ChecklistView.as_view(), name="index"),
]