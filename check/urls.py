from . import views
from django.urls import path

urlpatterns = [
    path("", views.ChecklistView.as_view(), name="checklist"),
    path("", views.BirdView.as_view(), name="birds"),
]