from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import Vitima


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, cpf=None, password=None):
        try:
            user = Vitima.objects.get(cpf=cpf)
            if not check_password(password, user.password):
                raise Vitima.DoesNotExist()
            return user
        except Vitima.DoesNotExist:
            return None
