from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    detail information about an account of user
    """
    user = models.ForeignKey(User)
    type = models.PositiveSmallIntegerField()
