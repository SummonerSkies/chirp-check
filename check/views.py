from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

# importing 
from .models import Bird, Checklist
from .forms import BirdForm, ChecklistForm

# Create your views here.
class HomePage(generic.TemplateView):
    """
    Displays the Chirp Check home page
    """
    template_name = 'base.html'

class ChecklistView(generic.ListView):
    """
    View for the Checklist model.
    """
    queryset = Checklist.objects.all()
    template_name ="check/index.html"


class BirdView(generic.ListView):
    """
    View for Birds model.
    """
    queryset = Bird.objects.all()
    template_name ="check/index.html"
