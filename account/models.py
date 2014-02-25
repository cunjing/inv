# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    more information about an account of user.
    """

    user_id = models.ForeignKey(User, unique=True, related_name='user_id')

    # account type
    # 1 investee, 2 investor, 3 service provider, 4 government
    account_type = models.PositiveSmallIntegerField()

    # current user's leader
    top_user_id = models.ForeignKey(User, default=0, related_name='top_user_id')

    # identity type
    # 0 leader, 1 secretary, 2 manager, 3 clerk, when top_user_id > 0.
    # default 0 means top_user_id == 0.
    identity_type = models.PositiveSmallIntegerField(default=0)

    # team name
    # company, organization, studio, ... 's name, when top_user_id == 0
    # if top_user_id == 0 and team_name == '', means this user is a leader for self without a team.
    team_name = models.CharField(max_length=100, default='', unique=True)
