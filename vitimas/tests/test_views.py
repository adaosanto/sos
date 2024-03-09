from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse_lazy
from model_bakery import baker

from ..models import Vitima


@pytest.fixture
def usuario_logado(db):
    user = baker.make(get_user_model(), email="tests@tests.com", is_superuser=True)
    user.set_password("tests")
    user.save()
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def vitima(db):
    return baker.make("Vitima", telefone="mealtera")


@pytest.fixture
def usuario_nao_logado(db):
    return Client()


@pytest.fixture
def form_valido(vitima):
    return {
        "nome": "FULANA DO TEST",
        "data_nascimento": str(date.today()),
        "rg": "542035",
        "cpf": "86530561579",
        "endereco": "Rua do fulano do test",
        "telefone": "65999999999",
        "suspeito": "Zé ninguém",
        "observacao": "nada",
    }


@pytest.fixture
def form_invalido(form_valido):
    form_invalido = form_valido.copy()
    form_invalido["cpf"] = "123456789"
    del form_invalido["nome"]
    return form_invalido


@pytest.mark.django_db
class TestListVitimasView:
    def test_vitima_output_do_tipo_json_deve_retorna_um_status_200(
        self, usuario_logado
    ):
        response = usuario_logado.get(reverse_lazy("vitimas"), data={"f": "json"})
        assert response.status_code == 200

    def test_vitima_output_do_tipo_json_deve_retorna_uma_lista_vazia(
        self, usuario_logado
    ):
        response = usuario_logado.get(reverse_lazy("vitimas"), data={"f": "json"})
        assert response.json()["data"] == []

    def test_usuario_nao_autenticado_deve_ser_redirecionado_status_302(
        self, usuario_nao_logado
    ):
        response = usuario_nao_logado.get(reverse_lazy("vitimas-new"))
        assert response.status_code == 302

    def test_quando_nao_especificado_o_output_deve_retorna_um_template(
        self, usuario_logado
    ):
        response = usuario_logado.get(reverse_lazy("vitimas"))
        assert "text/html" in response.headers["Content-Type"]
        assert "Vitimas" in response.content.decode()


@pytest.mark.django_db
class TestCreateVitimaView:
    def test_usuario_nao_autenticado_deve_ser_redirecionado_status_302(
        self, usuario_nao_logado
    ):
        response = usuario_nao_logado.get(reverse_lazy("vitimas"))
        assert response.status_code == 302

    def test_formulario_valido_deve_cadastrar_a_vitima_no_banco_de_dados(
        self, usuario_logado, form_valido
    ):
        response = usuario_logado.post(reverse_lazy("vitimas-new"), data=form_valido)
        assert Vitima.objects.filter(cpf=form_valido["cpf"]).exists()

    def test_formulario_invalido_nao_deve_cadastrar_a_vitima_no_banco_de_dados(
        self, usuario_logado, form_invalido
    ):
        response = usuario_logado.post(reverse_lazy("vitimas-new"), data=form_invalido)
        assert not Vitima.objects.filter(cpf=form_invalido["cpf"]).exists()


@pytest.mark.django_db
class TestChangeVitimaView:
    def test_usuario_nao_autenticado_deve_ser_redirecionado_status_302(
        self, usuario_nao_logado, vitima
    ):
        response = usuario_nao_logado.get(
            reverse_lazy("vitimas-edit", kwargs={"pk": vitima.id})
        )
        assert response.status_code == 302

    def test_formulario_invalido_nao_deve_atualizar_a_vitima_no_banco_de_dados(
        self, usuario_logado, vitima
    ):
        response = usuario_logado.post(
            reverse_lazy("vitimas-edit", kwargs={"pk": vitima.id}),
            data={
                "telefone": "65999999999"
            },  # Falta fornecer os campos is_active e endereço setado com obrigatórios
        )
        vitima.refresh_from_db()
        assert vitima.telefone != "65999999999"

    def test_formulario_valido_deve_atualizar_a_vitima_no_banco_de_dados(
        self, usuario_logado, vitima
    ):
        response = usuario_logado.post(
            reverse_lazy("vitimas-edit", kwargs={"pk": vitima.id}),
            data={
                "id": vitima.id,
                "telefone": "65999999999",
                "is_active": True,
                "endereco": "Rua do fulano",
                "observacao": "xpto",
            },
        )
        vitima.refresh_from_db()
        assert vitima.telefone == "65999999999"


@pytest.mark.django_db
class TestDetailVitimaView:
    def test_usuario_nao_autenticado_deve_ser_redirecionado_status_302(
        self, usuario_nao_logado, vitima
    ):
        response = usuario_nao_logado.get(
            reverse_lazy("vitima-detail", kwargs={"pk": vitima.id})
        )
        assert response.status_code == 302

    def test_quando_chamar_o_detail_da_view_o_nome_e_outras_informacoes_deve_estar_no_template(
        self, usuario_logado, vitima
    ):
        response = usuario_logado.get(
            reverse_lazy("vitima-detail", kwargs={"pk": vitima.id})
        )
        assert vitima.nome in response.content.decode()
        assert vitima.telefone in response.content.decode()
        assert vitima.cpf in response.content.decode()
