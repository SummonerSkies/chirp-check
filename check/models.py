from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Checklist(models.Model):
    """
    Represents a user-created checklist, including location and date.
    """
    list_name = models.CharField(max_length=75, blank=False, unique=True, help_text="Name your bird watching trip (Max 75 characters)")
    description = models.CharField(max_length=200, blank=False, help_text="Bird Watching Location (Max 200 characters)")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.list_name

class Bird(models.Model):
    bird = models.CharField(max_length=100, blank=False, Unique=True,)
    status = models.CharField(
        max_length=8,
        default="Not Seen",
        choices=[
            ("Not Seen", "Not Seen"),
            ("Spotted", "Spotted"),
        ],
        help_text="Did you see any?"
            "(choices: Not Seen, Spotted)"
    )
    number_seen = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    check_list = models.ForeignKey(Checklist)

    def __str__(self):
        return self.bird