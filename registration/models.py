from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)