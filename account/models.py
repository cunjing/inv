# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    more information about an account of user.
    """

    user_id = models.ForeignKey(User, unique=True, primary_key=True, db_column='user_id', related_name='user')

    # account type
    # 1 investee, 2 investor, 3 service provider, 4 government
    account_type = models.PositiveSmallIntegerField()

    # current user's leader
    top_user_id = models.ForeignKey(User, default=0, db_column='top_user_id', related_name='top_user')

    # identity type
    # 0 leader, 1 secretary, 2 manager, 3 clerk, when top_user_id > 0.
    # default 0 means top_user_id == 0.
    identity_type = models.PositiveSmallIntegerField(default=0)
