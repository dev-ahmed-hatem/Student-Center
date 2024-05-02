from base.models import UserProfile, User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password


class UserProfileBackend(BaseBackend):
    def authenticate(self, request, password, **kwargs):
        try:
            user = None
            if kwargs.get("username"):
                user = User.objects.get(username=kwargs["username"])
            elif kwargs.get("phone"):
                user = User.objects.get(userprofile=UserProfile.objects.get(phone=kwargs["phone"]))

            if user and check_password(password, user.password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
