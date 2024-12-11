from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from check.models import Checklist, Bird

# test views below

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.checklist = Checklist.objects.create(
            list_name="My Bird Checklist",
            description="A list of birds I have spotted.",
            user=self.user
        )
        self.bird = Bird.objects.create(
            bird_name="Sparrow",
            status="Spotted",
            number_seen=5,
            user=self.user,
            check_list=self.checklist
        )

    """
    checklist view tests
    """
    def test_checklist_view_url_exists(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_checklist_view_get(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check/index.html')
        self.assertContains(response, "My Bird Checklist")

    def test_checklist_view_redirect_if_not_logged_in(self):
        url = reverse('chirpcheck:index')
        response = self.client.get(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    """
    checklist create tests
    """
    def test_create_checklist_view_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:create')
        data = {'list_name': 'New Checklist', 'description': 'A new bird checklist'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertRedirects(response, reverse('chirpcheck:index'))
        self.assertTrue(Checklist.objects.filter(list_name='New Checklist').exists())

    def test_create_checklist_view_invalid_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:create')
        data = {'list_name': '', 'description': 'A new bird checklist'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check/create_checklist.html')
        self.assertFormError(response, 'checklist_form', 'list_name', 'This field is required.')

    def test_create_checklist_view_redirect_if_not_logged_in(self):
        url = reverse('chirpcheck:create')
        response = self.client.get(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_edit_checklist_view_get(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:edit_checklist', args=[self.checklist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check/edit_checklist.html')
        self.assertContains(response, "My Bird Checklist")

    def test_edit_checklist_view_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:edit_checklist', args=[self.checklist.id])
        data = {'list_name': 'Updated Checklist', 'description': 'Updated description'}
        response = self.client.post(url, data)
        self.checklist.refresh_from_db()
        self.assertEqual(self.checklist.list_name, 'Updated Checklist')
        self.assertEqual(self.checklist.description, 'Updated description')
        self.assertRedirects(response, reverse('chirpcheck:checklist', args=[self.checklist.id]))

    def test_edit_checklist_view_invalid_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:edit_checklist', args=[self.checklist.id])
        data = {'list_name': '', 'description': 'Updated description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check/edit_checklist.html')
        self.assertFormError(response, 'checklist_form', 'list_name', 'This field is required.')

    def test_edit_checklist_view_redirect_if_not_logged_in(self):
        url = reverse('chirpcheck:edit_checklist', args=[self.checklist.id])
        response = self.client.get(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_edit_checklist_view_permissions(self):
        original_user = User.objects.create_user(username='owner', password='password')
        checklist = Checklist.objects.create(list_name='Test Checklist', user=original_user)
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        url = reverse('chirpcheck:edit_checklist', args=[checklist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chirpcheck:index'))

    """
    Checklist delete tests
    """
    def test_delete_checklist_view_get(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:delete_checklist', args=[self.checklist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check/confirm_checklist_delete.html')

    def test_delete_checklist_view_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:delete_checklist', args=[self.checklist.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('chirpcheck:index'))
        self.assertFalse(Checklist.objects.filter(id=self.checklist.id).exists())

    def test_delete_checklist_view_permissions(self):
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        url = reverse('chirpcheck:delete_checklist', args=[self.checklist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chirpcheck:index'))

    """
    Checklist: Add Bird tests
    """
    def test_add_bird_view_post_valid(self):
    # Test that a user can successfully add a new bird to their checklist
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:add_bird', args=[self.checklist.id])
    
    # Ensure the check_list field is included in the POST data
        data = {
            'bird_name': 'Robin',
            'status': 'Spotted',
            'number_seen': 3,
            'check_list': self.checklist.id  # Add check_list to the POST data
        }

        response = self.client.post(url, data)

        # Check for a successful redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chirpcheck:checklist', args=[self.checklist.id]))

        # Check that the bird was added to the checklist
        self.assertTrue(Bird.objects.filter(bird_name='Robin', check_list=self.checklist).exists())

        # Check for the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Robin has now been added to your checklist!')

    def test_add_bird_to_other_checklist(self):
        """Test that a user cannot add a bird to someone else's checklist"""
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_user_checklist = Checklist.objects.create(
            list_name="Other User's Bird Checklist",
            description="A list of birds spotted by another user.",
            user=other_user  # This checklist belongs to 'other_user', not 'testuser'
        )
    
        # Login as the 'testuser', who doesn't own this checklist
        self.client.login(username='testuser', password='password')
    
        url = reverse('chirpcheck:add_bird', args=[other_user_checklist.id])
        data = {'bird_name': 'Robin', 'status': 'Spotted', 'number_seen': 3}
    
        # Attempt to add a bird to another user's checklist
        response = self.client.post(url, data)
    
        # The response should be a redirect to the index page
        self.assertEqual(response.status_code, 302)  # Ensure it's a redirect (302)
        self.assertRedirects(response, reverse('chirpcheck:index'))  # Ensure it redirects to the index page
    
        # Verify that the error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You can only add birds to your own checklist!')

    def test_add_bird_view_post_invalid(self):
        """Test that the view properly handles invalid form submissions"""
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:add_bird', args=[self.checklist.id])
        
        # Missing required fields (e.g., bird_name)
        data = {'status': 'Spotted', 'number_seen': 3}
        
        response = self.client.post(url, data)
        
        # Check that the response is still the form, not a redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify that the form contains an error for the missing bird_name field
        self.assertFormError(response, 'bird_form', 'bird_name', 'This field is required.')

    def test_add_bird_view_permissions(self):
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        url = reverse('chirpcheck:add_bird', args=[self.checklist.id])
        response = self.client.post(url, {'bird_name': 'Robin', 'status': 'Spotted', 'number_seen': 3})
        self.assertRedirects(response, reverse('chirpcheck:index'))

    """
    Checklist: Update Bird tests
    """
    def test_update_bird_view_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:update_bird', args=[self.checklist.id, self.bird.id])
        data = {
            'status': 'Not Spotted',
            'number_seen': 10
        }
        response = self.client.post(url, data)
        self.bird.refresh_from_db()
        self.assertEqual(self.bird.status, 'Not Spotted')
        self.assertEqual(self.bird.number_seen, 10)
        self.assertRedirects(response, reverse('chirpcheck:checklist', args=[self.checklist.id]))

    def test_update_bird_view_post_permission_error(self):
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        url = reverse('chirpcheck:update_bird', args=[self.checklist.id, self.bird.id])
        response = self.client.post(url, {
            'status': 'Not Spotted',
            'number_seen': 10
        })
        self.assertEqual(self.bird.status, 'Spotted')
        self.assertEqual(self.bird.number_seen, 5)
        self.assertRedirects(response, reverse('chirpcheck:index'))

    """
    Checklist: Delete Bird tests
    """
    def test_delete_bird_view_post(self):
        self.client.login(username='testuser', password='password')
        url = reverse('chirpcheck:confirm_bird_delete', args=[self.checklist.id, self.bird.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('chirpcheck:checklist', args=[self.checklist.id]))
        checklist_response = self.client.get(reverse('chirpcheck:checklist', args=[self.checklist.id]))