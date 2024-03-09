from django.db import models
from rest_framework.authtoken.models import Token

from vitimas.models import Vitima


class CustomToken(Token):
    user = models.OneToOneField(
        Vitima, related_name="auth_token", on_delete=models.CASCADE
    )
