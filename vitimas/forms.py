from django import forms

from .models import Vitima


class VitimaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    class Meta:
        model = Vitima
        fields = [
            "nome",
            "rg",
            "cpf",
            "data_nascimento",
            "endereco",
            "telefone",
            "suspeito",
            "foto_vitima",
            "foto_suspeito",
            "observacao",
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}


class VitimaChangeForm(VitimaCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["nome"].required = False
        self.fields["rg"].required = False
        self.fields["suspeito"].required = False
        self.fields["cpf"].required = False
        self.fields["data_nascimento"].required = False
        self.fields["status_flag"].required = False

    class Meta:
        model = Vitima
        fields = "__all__"
        widgets = {
            "nome": forms.TextInput(attrs={"disabled": "disabled"}),
            "suspeito": forms.TextInput(attrs={"disabled": "disabled"}),
            "cpf": forms.TextInput(attrs={"disabled": "disabled"}),
            "rg": forms.TextInput(attrs={"disabled": "disabled"}),
            "data_nascimento": forms.DateInput(attrs={"disabled": "disabled"}),
        }

    def clean_field(self, field_name):
        instance = getattr(self, "instance", None)
        if instance:
            return getattr(instance, field_name)
        else:
            return self.cleaned_data.get(field_name, None)

    def clean_nome(self):
        return self.clean_field("nome")

    def clean_suspeito(self):
        return self.clean_field("suspeito")

    def clean_cpf(self):
        return self.clean_field("cpf")

    def clean_rg(self):
        return self.clean_field("rg")

    def clean_data_nascimento(self):
        return self.clean_field("data_nascimento")
