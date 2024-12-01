from django import forms
from .models import Bird
from .models import Checklist

class ChecklistForm(forms.ModelForm):
    """
    Form class for creating a new checklist
    """
    class Meta:
        """
        Specify the django model and order of the checklist fields
        """
        model = Checklist
        fields = ('list_name', 'description')

class BirdForm(forms.ModelForm):
    """
    Form class for adding birds to a checklist
    """
    class Meta:
        """
        Specify the django model and order of the 'bird' fields
        """
        model = Bird
        fields = ('bird_name', 'status', 'number_seen', 'check_list')