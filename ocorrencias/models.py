from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from vitimas.models import Vitima


class Ocorrencia(models.Model):
    """
    Modelo para armazenar informações sobre uma ocorrência relacionada a uma vítima.
    """

    vitima = models.ForeignKey(Vitima, on_delete=models.CASCADE)
    data = models.DateTimeField("Data", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField("Lat", max_digits=20, decimal_places=10)
    longitude = models.DecimalField("Lon", max_digits=20, decimal_places=10)

    status_flag = models.CharField("Status Flag", max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Ocorrencia"
        verbose_name_plural = "Ocorrencias"


@receiver(pre_save, sender=Ocorrencia)
def set_status_flag(sender, instance, **kwargs):
    if instance.is_active:
        instance.status_flag = '<span class="fa fa-check-square-o fa-lg" style="color:green; font-size:20px;"></span>'

    if not instance.is_active:
        instance.status_flag = '<span class="fa fa-square-o fa-lg" style="color:red; font-size:20px;"></span>'
