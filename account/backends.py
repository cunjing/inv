from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthBackend(ModelBackend):
    """
    Authentication by email.
    """

    def authenticate(self, email=None, password=None, username=None, is_staff=None):
        """
        email for frontend, or username for backend
        @return User
        """
        rtn = None
        if email is not None:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(username=username)
        if user is not None and user.check_password(password):
            if is_staff is not None:
                if user.is_staff == is_staff:
                    rtn = user
                else:
                    rtn = None
            else:
                rtn = user
        return rtn
