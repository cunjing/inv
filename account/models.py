# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    more information about an account of user.
    """

    user_id = models.ForeignKey(User, unique=True)

    # account type
    # 1 investee, 2 investor, 3 service provider, 4 government
    account_type = models.PositiveSmallIntegerField()

    # is team?
    # 0 not a team, 1 is a team
    is_team = models.BooleanField(default=0)

    # current user's leader
    # top_user_id == 0 when is_team == 1
    top_user_id = models.ForeignKey(User, default=0)

    # identity type
    # 1 secretary, 2 manager, 3 clerk, when top_user_id > 0.
    # default 0 means top_user_id == 0 and this user has no leader.
    identity_type = models.PositiveSmallIntegerField(default=0)


class Team(models.Model):
    """
    team managed by an account of user.
    this user's Profile.is_team == 1 and Profile.top_user_id == 0 and Profile.identity_type == 0.
    """

    user_id = models.ForeignKey(User, unique=True)

    # team name
    # company, organization, studio, ... 's name
    team_name = models.CharField(max_length=100, default='', unique=True)
