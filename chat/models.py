from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length = 200)
    documentContent = models.TextField(null = True, blank = True)
    embedding = models.TextField()

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = models.TextField()
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
