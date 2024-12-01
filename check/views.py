# chirp_check/check/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import Bird, Checklist
from .forms import BirdForm, ChecklistForm

# Create your views here.
class HomePage(TemplateView):
    """
    Displays the Chirp Check home page
    """
    template_name = 'base.html'

class ChecklistView(ListView):
    """
    View for the Checklist model.
    """
    model = Checklist
    template_name ="check/index.html"


class BirdView(ListView):
    """
    View for Birds model.
    """
    model = Bird
    template_name =""
