# models.py
from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
