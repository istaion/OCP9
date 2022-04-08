from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    follows = models.ManyToManyField('self',
                                     through='review.UserFollows',
                                     symmetrical=False,
                                     related_name='followed')
