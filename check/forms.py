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
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'list_name': 'Checklist Name',  # Clarifying what the user should input
            'description': 'Bird watching location',
        }


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
    # Hide check_list field as it should already be associated with the checklist
		widgets = {
            	'check_list': forms.HiddenInput(),
		}
		labels = {
			'bird_name': 'Name of Bird',
			'status': 'Did You See It?',  
			'number_seen': 'Number of Birds Seen'
		}