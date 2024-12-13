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
        labels = {
            'list_name': 'Checklist Name',
            'description': 'Bird Watching Location',
        }

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
        model = Bird
        fields = ['bird_name', 'status', 'number_seen', 'check_list']
        widgets = {
            'check_list': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        bird_name = cleaned_data.get('bird_name')
        check_list = cleaned_data.get('check_list')

        # Get the current bird instance (if any)
        current_bird = self.instance

        # Check if the bird already exists in the checklist,
        # but exclude the current bird
        if Bird.objects.filter(
            bird_name=bird_name, check_list=check_list).exclude(
                id=current_bird.id).exists():
            raise forms.ValidationError(
                "This bird already exists in your checklist.")

        return cleaned_data
