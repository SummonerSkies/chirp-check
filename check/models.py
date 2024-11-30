from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Checklist(models.Model):
    """
    Represents a user-created checklist, including location and date.
    """
    list_name = models.CharField(max_length=75, blank=False, unique=True, help_text="Name your bird watching trip (Max 75 characters)")
    description = models.CharField(max_length=200, blank=False, unique=False, help_text="Bird Watching Location (Max 200 characters)")
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.list_name