# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    more information about an account of user.
    """

    user = models.OneToOneField(User, primary_key=True)

    # see dict _user_type_allowed
    user_type = models.PositiveSmallIntegerField()

    # current user's leader
    leader = models.ForeignKey(User, default=0, related_name='leader')

    # identity Type: 1 secretary, 2 manager, 3 clerk
    # identity type default 0 means top_user_id == 0, and current user is a leader.
    # when top_user_id > 0, this field must be greater than 0, and in IdentityType list.
    identity_type = models.PositiveSmallIntegerField(default=0)

    _user_type_allowed = {
        1: u'investee',
        2: u'investor',
        3: u'service provider',
        4: u'government',
    }

    def __unicode__(self):
        return self._user_type_allowed.get(self.user_type)
