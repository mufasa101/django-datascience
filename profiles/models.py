from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, verbose_name="profile_user", on_delete=models.CASCADE)
    bio=models.TextField(blank=True,null=True)
    avatar=models.ImageField(help_text="profile avatar", upload_to="medial")
    @property
    def get_full_name(self):
        full_name=f'{self.user.first_name} {self.user.last_name}'
        return full_name
    def __str__(self):
        return f'profile for: {self.user.first_name}'
    