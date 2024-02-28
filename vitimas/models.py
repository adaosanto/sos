import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from stdimage import StdImageField


def get_file_path(_instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


class BaseModel(models.Model):
    """
    Classe base para modelos com campos compartilhados.
    """

    is_active = models.BooleanField(default=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_edition = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vitima(BaseModel):
    """
    Modelo para armazenar informações sobre uma vítima.
    """

    nome = models.CharField("Nome", max_length=120, null=False)
    rg = models.CharField("Registro Geral", max_length=10, null=False)
    cpf = models.CharField("CPF", max_length=14, null=False, unique=True)
    data_nascimento = models.DateField("Data de Nascimento", null=False)
    endereco = models.CharField("Endereço", max_length=120, null=False)
    telefone = models.CharField("Telefone", max_length=18, null=False)
    suspeito = models.CharField("Suspeito", max_length=120, null=False)
    chave_acesso = models.CharField(max_length=15, default="", editable=False)
    status_flag = models.CharField("Status Flag", max_length=200, null=False)
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
    observacao = models.TextField("Observações", null=True, blank="")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Vitima"
        verbose_name_plural = "Vitimas"


@receiver(pre_save, sender=Vitima)
def vitima_pre_save(instance, sender, **kwargs):
    """
    Sinal pré-salvar para atualizar a chave de acesso da vítima.
    """
    instance.chave_acesso = instance.cpf[:3] + instance.data_nascimento.strftime(
        "%d%m%Y"
    )


@receiver(pre_save, sender=Vitima)
def set_status_flag(sender, instance, **kwargs):
    if instance.is_active:
        instance.status_flag = '<span class="fa fa-check-square-o fa-lg" style="color:green; font-size:20px;"></span>'

    if not instance.is_active:
        instance.status_flag = '<span class="fa fa-square-o fa-lg" style="color:red; font-size:20px;"></span>'
