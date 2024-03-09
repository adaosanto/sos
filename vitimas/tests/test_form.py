import pytest
from django import forms
from model_bakery import baker

from ..forms import VitimaChangeForm, VitimaCreateForm


@pytest.fixture
def form():
    return VitimaChangeForm()


@pytest.fixture
def vitima_instance():
    return baker.make("Vitima")


@pytest.fixture
def filled_form(vitima_instance):
    return VitimaChangeForm(instance=vitima_instance)


@pytest.mark.django_db
class TestFormVitimaCreateForm:
    def test_form_verifica_se_um_campo_tem_o_atributo_form_control(self):
        form = VitimaCreateForm()
        for field_name, field in form.fields.items():
            assert "form-control" in field.widget.attrs.get("class", [])

    def test_verifica_se_o_campo_data_nascimento_tem_a_instacia_de_DateInput(self):
        form = VitimaCreateForm()
        assert isinstance(form.fields["data_nascimento"].widget, forms.DateInput)


@pytest.mark.django_db
class TestFormVitimaChangeForm:
    def test_form_verifica_se_um_campo_tem_o_atributo_form_control(self, form):
        for field_name, field in form.fields.items():
            assert "form-control" in field.widget.attrs.get("class", [])

    def test_verifica_se_um_campo_esta_como_não_requerido_form(self, form):
        campos = ["nome", "rg", "suspeito", "cpf", "data_nascimento", "status_flag"]
        for campo in campos:
            assert not form.fields[campo].required

    @pytest.mark.parametrize(
        "field_name", ["nome", "rg", "suspeito", "cpf", "data_nascimento", "password"]
    )
    def test_clean_field_method(self, filled_form, vitima_instance, field_name):
        assert filled_form.clean_field(field_name) == getattr(
            vitima_instance, field_name
        )

    @pytest.mark.parametrize(
        "method_name",
        [
            "clean_nome",
            "clean_rg",
            "clean_suspeito",
            "clean_cpf",
            "clean_data_nascimento",
        ],
    )
    def test_clean_method(self, filled_form, vitima_instance, method_name):
        assert getattr(filled_form, method_name)() == getattr(
            vitima_instance, method_name.replace("clean_", "")
        )

    def test_clean_method_password(self, filled_form, vitima_instance):
        assert filled_form.clean_data_password() is not None
