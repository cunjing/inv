# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    """
    user type
    investee, investor, service provider, government
    """

    class Meta:
        db_table = 'account_user_type'

    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class IdentityType(models.Model):
    """
    identity Type
    leader, secretary, manager, clerk
    identity type default 0 means Profile.leader == 0, and current user is a leader.
    when Profile.leader > 0, the field Profile.identity_type must be greater than 0.
    """

    class Meta:
        db_table = 'account_identity_type'

    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    """
    more information about an account of user.
    """

    user = models.OneToOneField(User, primary_key=True)
    user_type = models.ForeignKey(UserType)
    leader = models.ForeignKey(User, default=0, related_name='leader')  # user's leader
    identity_type = models.ForeignKey(IdentityType, default=0)
