from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    test_information = models.JSONField()

    def __str__(self):
        return f"{self.user.username} Profile"
