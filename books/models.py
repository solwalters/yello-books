from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token


class Author(AbstractUser):
    name = models.CharField(max_length=200)
    pseudonym = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.pseudonym or self.name or self.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    cover_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return "\"{0}\" - By {1}".format(self.title, self.author)
