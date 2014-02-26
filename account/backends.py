# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthBackend(ModelBackend):
    """
    Authentication backend with email override username.
    """

    def authenticate(self, email=None, password=None, username=None, is_staff=None):
        """
        authenticate user's identity.

        @param (string) email    for frontend
        @param (string) password
        @param (string) username for django admin (backend)
        @param (bool)   is_staff

        @return (User)
        """

        rtn = None

        try:
            if email is not None:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            if is_staff is not None:
                if user.is_staff == is_staff:
                    rtn = user
            else:
                rtn = user

        return rtn
