from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Document(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    download_count = models.PositiveIntegerField(default=0)
    email_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class DownloadLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)


class EmailLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    recipient = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
