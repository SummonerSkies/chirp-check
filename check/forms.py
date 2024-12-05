from django import forms
from .models import Bird, Checklist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
        # labels = {
        #     'list_name': 'Checklist Name',
        #     'description': 'Bird Watching Location',
        # }
        
    def __init__(self, *args, **kwargs):
        super(ChecklistForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create Checklist'))


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
    # Hide check_list field as this form should already be associated with the checklist
        # widgets = {
        #     'check_list': forms.HiddenInput(),
        # }
        # labels = {
		# 	'bird_name': 'Name of Bird',
		# 	'status': 'Did You See It?',  
		# 	'number_seen': 'Number of Birds Seen'
		# }