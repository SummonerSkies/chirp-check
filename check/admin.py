from django.contrib import admin
from .models import Bird, Checklist

# Register your models here.
admin.site.register(Checklist)
admin.site.register(Bird)