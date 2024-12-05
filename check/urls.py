from . import views
from django.urls import path, include

app_name = 'chirpcheck'

urlpatterns = [
    path("", views.ChecklistView.as_view(), name="index"),
    path("", views.BirdView.as_view(), name="birds"),
    path("chirpcheck/create/", views.create_checklist, name="create"),
    path('chirpcheck/edit/<int:id>', views.edit_checklist, name='edit_checklist'),
    path('chirpcheck/delete/<int:id>/', views.delete_checklist, name='delete_checklist'),
    path('chirpcheck/<int:checklist_id>/add_bird/', views.add_bird, name='add_bird'),
    path("chirpcheck/<id>/", views.my_checklist, name="checklist"),
]