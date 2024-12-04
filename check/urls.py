from . import views
from django.urls import path, include

app_name = 'chirpcheck'

urlpatterns = [
    path("", views.ChecklistView.as_view(), name="index"),
    path("", views.BirdView.as_view(), name="birds"),
    path("chirpcheck/<id>/", views.my_checklist, name="checklist"),
]