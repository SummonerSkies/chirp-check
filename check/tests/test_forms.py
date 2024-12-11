from django.test import TestCase
from django.contrib.auth.models import User
from check.forms import BirdForm, ChecklistForm
from check.models import Bird, Checklist

class TestForms(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.checklist = Checklist.objects.create(
            list_name='Test Checklist',
            description='Test Location',
            user=self.user
        )

    # ChecklistForm Tests
    def test_checklist_form_valid_data(self):
        form = ChecklistForm(data={
            'list_name': 'My First Watch',
            'description': 'At Home',
        })
        self.assertTrue(form.is_valid())
    
    def test_checklist_form_no_data(self):
        form = ChecklistForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
    
    def test_checklist_form_invalid_data(self):
        form = ChecklistForm(data={
            'list_name': '',
            'description': 'At Home',
        })
        self.assertFalse(form.is_valid())  # Should be invalid because list_name is required
        self.assertIn('list_name', form.errors)  # Check that the correct field is in errors

    # BirdForm Tests
    def test_bird_form_valid_data(self):
        # Create a Bird object with user and checklist association
        form = BirdForm(data={
            'bird_name': 'Sparrow',
            'status': 'Not Seen',  # Use a valid status choice
            'number_seen': 3,
            'check_list': self.checklist.id,  # Reference the checklist ID
            'user': self.user.id,  # Ensure the user is included
        })
        self.assertTrue(form.is_valid())  # The form should be valid when all fields are correct

    def test_bird_form_duplicate_bird(self):
        # First, create a bird in the checklist
        Bird.objects.create(
            bird_name='Sparrow',
            status='Not Seen',
            number_seen=5,
            check_list=self.checklist,
            user=self.user  # Make sure to associate the user with the Bird
        )

        # Now, try to add the same bird to the checklist
        form = BirdForm(data={
            'bird_name': 'Sparrow',  # Same name as the previous bird
            'status': 'Not Seen',  # Use the same valid status
            'number_seen': 3,
            'check_list': self.checklist.id,
            'user': self.user.id,
        })

        self.assertFalse(form.is_valid())  # Should be invalid because the bird already exists
        self.assertIn('__all__', form.errors)  # Check that the non-field error is present
        self.assertEqual(form.errors['__all__'][0], "This bird already exists in your checklist.")  # Verify the exact error message