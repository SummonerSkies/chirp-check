from django.test import SimpleTestCase
from django.urls import reverse, resolve
from check import views

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('chirpcheck:index')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, views.ChecklistView)

    def test_edit_checklist_url_is_resolved(self):
        url = reverse('chirpcheck:edit_checklist', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolve(url).func, views.edit_checklist)

    def test_delete_checklist_url_is_resolved(self):
        url = reverse('chirpcheck:delete_checklist', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolve(url).func, views.delete_checklist)

    def test_add_bird_url_is_resolved(self):
        url = reverse('chirpcheck:add_bird', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolve(url).func, views.add_bird)

    def test_update_bird_url_is_resolved(self):
        url = reverse('chirpcheck:update_bird', args=[1, 25])
        resolved_view = resolve(url)
        self.assertEqual(resolve(url).func, views.update_bird)

    def test_delete_bird_url_is_resolved(self):
        url = reverse('chirpcheck:confirm_bird_delete', args=[1, 25])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, views.delete_bird)

    def test_my_checklist_url_is_resolved(self):
        url = reverse('chirpcheck:checklist', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, views.my_checklist)