import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse_lazy
from model_bakery import baker

from ..models import Ocorrencia


@pytest.fixture
def ocorrencias(db):
    return baker.make(Ocorrencia, _quantity=15)


@pytest.fixture
def usuario(db):
    return baker.make(get_user_model())


@pytest.fixture
def client_logado(usuario):
    client = Client()
    client.force_login(usuario)
    return client


class TestListOcorrenciasView:
    def test_quando_o_usuario_nao_fornecer_o_format_um_template_devera_ser_retornado(
        self, client_logado
    ):
        response = client_logado.get(reverse_lazy("ocorrencias"))
        assert "text/html" in response.headers["Content-Type"]

    def test_quando_o_usuario_fornecer_o_format_como_json_um_json_devera_ser_retornado(
        self, client_logado, ocorrencias
    ):
        response = client_logado.get(reverse_lazy("ocorrencias"), data={"f": "json"})
        assert "application/json" in response.headers["Content-Type"]
        assert len(response.json()["data"]) == len(ocorrencias)

    def test_quando_o_usuario_esta_inativo_deve_atualizar_o_campo_status_flag(
        self, client_logado, ocorrencias
    ):
        ocorrencia = ocorrencias[-1]
        ocorrencia.is_active = False
        ocorrencia.save()

        assert (
            ocorrencia.status_flag
            == '<span class="fa fa-square-o fa-lg" style="color:red; font-size:20px;"></span>'
        )
