from . import views
from django.urls import path, include

app_name = 'chirpcheck'

urlpatterns = [
    path("", views.ChecklistView.as_view(), name="index"),
    path("chirpcheck/create/", views.create_checklist, name="create"),
    path('chirpcheck/edit/<int:id>', views.edit_checklist, name='edit_checklist'),
    path('chirpcheck/delete/<int:id>/', views.delete_checklist, name='delete_checklist'),
    path('chirpcheck/<int:checklist_id>/add_bird/', views.add_bird, name='add_bird'),
    path('chirpcheck/<int:checklist_id>/update_bird/<int:bird_id>/', views.update_bird, name='update_bird'),
    path('chirpcheck/<int:checklist_id>/delete_bird/<int:bird_id>/', views.delete_bird, name='confirm_bird_delete'),
    path("chirpcheck/<id>/", views.my_checklist, name="checklist"),
]