from django.db import models

# Create your models here.

class UserSession(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    context = models.JSONField(default=dict)  # Store conversation context as a dictionary

    def __str__(self):
        return f"Session for user {self.user_id}"
