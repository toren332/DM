from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class PhoneCode(models.Model):
    phone = models.PositiveIntegerField(validators=[MinValueValidator(70000000000), MaxValueValidator(79999999999)], unique=True)
    code = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return 'Phone: '+ str(self.phone) + '; Code: ' + str(self.code) + '; Verified: ' + str(self.is_verified)
