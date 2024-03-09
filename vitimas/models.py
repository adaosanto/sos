import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from stdimage import StdImageField
from random import randint

def get_file_path(_instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, password):
        user = self.model(cpf=cpf)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Vitima(AbstractBaseUser):
    """
    Modelo para armazenar informações sobre uma vítima.
    """

    cpf = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_edition = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    chave_acesso = models.CharField(max_length=15, default='', editable=False)
    nome = models.CharField("Nome", max_length=120, null=False)
    rg = models.CharField("Registro Geral", max_length=10, null=False)
    data_nascimento = models.DateField("Data de Nascimento", null=False)
    endereco = models.CharField("Endereço", max_length=120, null=False)
    telefone = models.CharField("Telefone", max_length=18, null=False)
    suspeito = models.CharField("Suspeito", max_length=120, null=False)
    status_flag = models.CharField(
        "Status Flag", max_length=200, blank=True, default=""
    )
    foto_vitima = StdImageField(
        "Foto da Vítima",
        upload_to=get_file_path,
        default="avatarPadraoVitima.jpg",
        variations={
            "thumb": {"width": 212, "height": 212, "crop": True, "resample": True}
        },
    )
    foto_suspeito = StdImageField(
        "Foto do Suspeito",
        upload_to=get_file_path,
        default="avatarPadraoSuspeito.jpg",
        variations={
            "thumb": {"width": 212, "height": 212, "crop": True, "resample": True}
        },
    )
    observacao = models.TextField("Observações", null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "cpf"

    def __str__(self):
        return self.cpf

    class Meta:
        verbose_name = "Vitima"
        verbose_name_plural = "Vitimas"


@receiver(pre_save, sender=Vitima)
def set_status_flag(sender, instance, **kwargs):
    if instance.is_active:
        instance.status_flag = '<span class="fa fa-check-square-o fa-lg" style="color:green; font-size:20px;"></span>'

    if not instance.is_active:
        instance.status_flag = '<span class="fa fa-square-o fa-lg" style="color:red; font-size:20px;"></span>'


@receiver(pre_save, sender=Vitima)
def set_chave_acesso(sender, instance, **kwargs):
    chave = ""
    for _ in range(8):
        chave += str(randint(0, 9))
    if len(instance.chave_acesso) == 0:
        instance.chave_acesso = chave        
@receiver(pre_save, sender=Vitima)
def set_password(sender, instance, **kwargs):
    instance.set_password(instance.chave_acesso)