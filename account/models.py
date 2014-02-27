# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    """
    user type.
    1 investee, 2 investor, 3 service provider, 4 government
    """

    title = models.CharField(max_length=20)


class IdentityType(models.Model):
    """
    identity Type.
    1 secretary, 2 manager, 3 clerk
    """

    title = models.CharField(max_length=20)


class Profile(models.Model):
    """
    more information about an account of user.
    """

    user_id = models.ForeignKey(User, unique=True, primary_key=True, db_column='user_id', related_name='user')
    user_type_id = models.ForeignKey(UserType, db_column='user_type_id', related_name='user_type')

    # current user's leader
    top_user_id = models.ForeignKey(User, default=0, db_column='top_user_id', related_name='top_user')

    # identity type default 0 means top_user_id == 0, and current user is a leader.
    # when top_user_id > 0, this field must be greater than 0, and in IdentityType list.
    identity_type_id = models.ForeignKey(IdentityType, default=0, db_column='identity_type_id', related_name='identity_type')
