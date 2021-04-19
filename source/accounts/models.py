from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics')
    info = models.TextField(max_length=300,null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - github{self.github}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'