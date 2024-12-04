from . import views
from django.urls import path

urlpatterns = [
    path("", views.ChecklistView.as_view(), name="index"),
    path("", views.BirdView.as_view(), name="birds"),
    path("list/<int:check_id>/", views.ListChecklistView.as_view(), name="checklist"),
]