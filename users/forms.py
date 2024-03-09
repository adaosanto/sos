from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UsernameField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from validate_docbr import CPF

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "E-mail",
                "value": "",
                "id": "email",
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "value": "", "placeholder": "Senha"}
        ),
    )

    error_messages = {
        "invalid_login": _("E-mail ou senha incorretos."),
        "inactive": _("Conta inativa"),
    }


class UserMeCustomChangeForm(UserChangeForm):
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "value": "", "placeholder": "Senha"}
        ),
    )
    foto = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control", "placeholder": "Sua foto"}
        ),
    )

    class Meta:
        model = User
        fields = ["genero", "foto", "password"]
        widgets = {
            "genero": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_password(self):
        # Obtenha a senha original do usuário
        new_password = self.cleaned_data["password"]
        original_password = self.instance.password

        # Se o campo de senha estiver vazio, retorne a senha original
        if len(new_password) == 0:
            return original_password

        # Caso contrário, retorne a nova senha
        return make_password(new_password)


class UserCustomChangeForm(UserMeCustomChangeForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["is_active"]:
                self.fields[field].widget.attrs["class"] = "form-control"

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not CPF().validate(cpf):
            raise ValidationError(
                self.error_messages["cpf_invalido"],
                code="cpf_invalido",
            )
        return cpf

    class Meta:
        model = User
        fields = [
            "nome",
            "email",
            "telefone",
            "password",
            "genero",
            "is_active",
            "foto",
            "groups",
        ]


class UserCustomUserCretionForm(forms.ModelForm):
    """
    Formulário para editar os detalhes de um usuário existente.
    """

    error_messages = {
        "cpf_invalido": ("CPF inválido."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not CPF().validate(cpf):
            raise ValidationError(
                self.error_messages["cpf_invalido"],
                code="cpf_invalido",
            )
        return cpf

    class Meta:
        model = User
        fields = [
            "nome",
            "email",
            "password",
            "cpf",
            "telefone",
            "genero",
            "foto",
            "groups",
        ]
        widgets = {"password": forms.PasswordInput()}
