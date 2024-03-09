import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from stdimage import StdImageField

from django.urls import reverse_lazy

def get_file_path(_instance, filename):
    """
    Função para gerar um caminho único para o upload de arquivos de imagem.
    """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


class CustomUserManager(UserManager):
    """
    Gerenciador personalizado para o modelo User.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Cria e salva um usuário com o e-mail e senha fornecidos.
        """
        if not email:
            raise ValueError("E-mail é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Cria um usuário comum.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Cria um superusuário.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo personalizado de usuário.
    """

    GENERO_CHOICES = (("M", "Masculino"), ("F", "Feminino"))
    email = models.EmailField("E-email", null=False, unique=True)
    nome = models.CharField("Nome", max_length=255, null=False)
    telefone = models.CharField("Telefone", max_length=15, null=False)
    cpf = models.CharField("CPF", max_length=14, null=False, unique=True)
    genero = models.CharField(
        "Gênero", max_length=1, null=False, choices=GENERO_CHOICES
    )
    foto = StdImageField(
        "Foto",
        upload_to=get_file_path,
        default='padrao.jpg',
        variations={"thumb": {"width": 512, "height": 512, "crop": True}},
        delete_orphans=True,
    )
    status_flag = models.CharField("Status Flag", max_length=200, null=False)
    is_active = models.BooleanField("Ativo?", default=True)
    is_superuser = models.BooleanField("Super Administrador?", default=False)
    is_staff = models.BooleanField("Administrador?", default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        """
        Retorna o nome completo do usuário.
        """
        return self.nome

    def get_short_name(self):
        """
        Retorna o nome curto do usuário (parte antes do '@' no e-mail).
        """
        return self.nome or self.email.split("@")[0]


@receiver(pre_save, sender=User)
def set_status_flag(sender, instance, **kwargs):
    if instance.is_active:
        instance.status_flag = '<span class="fa fa-check-square-o fa-lg" style="color:green; font-size:20px;"></span>'

    if not instance.is_active:
        instance.status_flag = '<span class="fa fa-square-o fa-lg" style="color:red; font-size:20px;"></span>'
