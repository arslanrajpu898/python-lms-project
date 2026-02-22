from django.db import models
from django.contrib.auth.models import User  # IMPORT THE USER!

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    file = models.FileField(upload_to='lesson_files/', null=True, blank=True) 
    content = models.TextField(null=True, blank=True) 
    video_url = models.CharField(max_length=500, null=True, blank=True) 
    
    # --- OUR NEW PROGRESS TRACKER ---
    # This creates a hidden link between Lessons and Users!
    completed_by = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return self.title

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"