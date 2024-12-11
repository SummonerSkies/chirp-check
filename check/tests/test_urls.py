from django.test import SimpleTestCase
from django.urls import reverse, resolve
from check import views

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('chirpcheck:index')
        print(resolve(url))