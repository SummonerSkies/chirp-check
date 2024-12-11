from django.test import TestCase
from django.contrib.auth.models import User
from check.models import Bird, Checklist

class ChecklistModelTest(TestCase):
    def setUp(self):
        """
        Set up the user and a checklist instance for testing.
        """
        self.user = User.objects.create_user(username='testuser', password='password')
        self.checklist = Checklist.objects.create(
            list_name="My Bird Checklist",
            description="A list of birds I have spotted.",
            user=self.user
        )

    def test_checklist_creation(self):
        """
        Test the creation of a Checklist instance.
        """
        self.assertEqual(self.checklist.list_name, "My Bird Checklist")
        self.assertEqual(self.checklist.description, "A list of birds I have spotted.")
        self.assertEqual(self.checklist.user.username, "testuser")
        self.assertTrue(isinstance(self.checklist, Checklist))

    def test_checklist_get_absolute_url(self):
        """
        Test the `get_absolute_url` method of the Checklist model.
        """
        self.assertEqual(self.checklist.get_absolute_url(), f"/chirpcheck/{self.checklist.id}/")

    def test_checklist_unique_constraint(self):
        """
        Test the unique constraint on 'list_name' for a user.
        """
        # Attempt to create a checklist with the same name for the same user
        with self.assertRaises(Exception):
            Checklist.objects.create(
                list_name="My Bird Checklist",
                description="Another checklist",
                user=self.user
            )

class BirdModelTest(TestCase):
    def setUp(self):
        """
        Set up a user, checklist, and bird instance for testing.
        """
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

    def test_bird_creation(self):
        """
        Test the creation of a Bird instance.
        """
        self.assertEqual(self.bird.bird_name, "Sparrow")
        self.assertEqual(self.bird.status, "Spotted")
        self.assertEqual(self.bird.number_seen, 5)
        self.assertEqual(self.bird.user.username, "testuser")
        self.assertEqual(self.bird.check_list.list_name, "My Bird Checklist")
        self.assertTrue(isinstance(self.bird, Bird))

    def test_bird_unique_constraint(self):
        """
        Test the unique constraint on 'bird_name' for a given checklist.
        """
        # Attempt to create a bird with the same name in the same checklist
        with self.assertRaises(Exception):
            Bird.objects.create(
                bird_name="Sparrow",
                status="Spotted",
                number_seen=3,
                user=self.user,
                check_list=self.checklist
            )
            
    def test_bird_str_method(self):
        """
        Test the `__str__` method of the Bird model.
        """
        self.assertEqual(str(self.bird), "Sparrow")