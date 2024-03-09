import pytest
from django.urls import reverse_lazy
from model_bakery import baker
from rest_framework.test import APIClient

from ocorrencias.models import Ocorrencia

from ..models import CustomToken


@pytest.fixture
def vitima(db):
    user = baker.make("Vitima")
    user.set_password("test")
    user.save()
    return user


@pytest.fixture
def token_valido(db, vitima):
    token = baker.make(CustomToken, user=vitima)

    return token


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestLoginAPIView:
    def test_quando_o_formulario_post_for_valido_deve_ser_status_200(
        self, vitima, client
    ):
        response = client.post(
            reverse_lazy("login-api-view"),
            data={"cpf": vitima.cpf, "password": vitima.chave_acesso},
            format="json",
        )
        assert response.status_code == 200

    def test_quando_o_formulario_post_for_invalido_deve_ser_status_401(
        self, client, vitima
    ):
        response = client.post(
            reverse_lazy("login-api-view"),
            data={"cpf": vitima.cpf, "password": "senha errada"},
            format="json",
        )

        assert response.status_code == 401


@pytest.mark.django_db
class TestOcorrenciaAPIView:
    def test_post_com_um_token_invalido_deve_receber_status_401(
        self, client, token_valido, vitima
    ):
        client.credentials(HTTP_AUTHORIZATION="Token Inválido" + token_valido.key)
        response = client.post(
            reverse_lazy("ocorrencia-api-view"),
            data=dict(vitima=vitima.id, latitude=-13.083, longitude=-55.906),
        )

        assert response.status_code == 401

    def test_quando_um_token_for_valido_deve_receber_status_201(
        self, client, token_valido, vitima
    ):
        client.credentials(HTTP_AUTHORIZATION="Token " + token_valido.key)
        response = client.post(
            reverse_lazy("ocorrencia-api-view"),
            data=dict(vitima=vitima.id, latitude=-13.083, longitude=-55.906),
        )

        assert response.status_code == 201
        assert Ocorrencia.objects.filter(vitima=vitima).exists()
