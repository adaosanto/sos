import pytest
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse_lazy
from faker import Faker
from model_bakery import baker

from app.views import HomePageView

from ..models import User
from ..views import LoginView


@pytest.fixture
def usuario_valido(db):
    user = baker.make(User, genero="F", is_superuser=True)
    user.set_password("test")
    user.save()

    baker.make(User, _quantity=10)
    return user


@pytest.fixture
def grupo_usuario(db):
    grupo, _ = Group.objects.get_or_create(name='Admin')
    return grupo

@pytest.fixture
def factory_data_fake():
    return Faker("pt_BR")


@pytest.fixture
def client(db):
    return Client()


@pytest.fixture
def client_logado(usuario_valido):
    client = Client()
    client.force_login(usuario_valido)
    return client


@pytest.fixture
def login_form_valido(usuario_valido):
    return {"username": usuario_valido.email, "password": "test"}


@pytest.fixture
def login_form_invalido(login_form_valido):
    form = login_form_valido.copy()
    form["password"] = "senha errada"
    return form


@pytest.mark.django_db
class TestLoginView:

    def test_usuario_invalido_deve_ser_redirecionando_para_a_mesma_url_de_login(
        self, client: Client, login_form_invalido
    ):
        response = client.post(reverse_lazy("login"), data=login_form_invalido)
        assert isinstance(response.context_data["view"], LoginView)

    def test_usuario_logado_nao_sera_redicionado_para_pagina_login(
        self, client: Client, login_form_valido
    ):
        response = client.post(
            reverse_lazy("login"), data=login_form_valido, follow=True
        )
        assert isinstance(response.context_data["view"], HomePageView)


@pytest.mark.django_db
class TestChangeMeView:

    def test_quando_o_usuario_acessar_a_pagina_sobre_me_dever_ter_no_context_data_as_client_ip_e_outras_infomacoes(
        self, client_logado
    ):
        response = client_logado.get(reverse_lazy("aboutme"), follow=True)
        assert bool(response.context_data.get("client_ip"))
        assert bool(response.context_data.get("expire_in"))

    def test_quando_o_usuario_acessar_a_pagina_a_instancia_de_seu_usuario_deve_estar_no_context_data(
        self, usuario_valido, client_logado
    ):
        response = client_logado.get(reverse_lazy("change_me"), follow=True)
        assert response.context_data["object"] == usuario_valido

    def test_quando_o_formulario_for_invalido_o_perfil_nao_deverá_ser_atualizado(
        self, usuario_valido, client_logado
    ):
        form = {}
        response = client_logado.post(reverse_lazy("change_me"), data=form, follow=True)
        usuario_valido.refresh_from_db()
        assert response.context_data["object"] == usuario_valido

    def test_quando_o_formulario_for_valido_o_perfil_deve_ser_atualizado(
        self, usuario_valido, client_logado
    ):
        form = {
            "genero": "M",
            "password": "",
        }
        response = client_logado.post(reverse_lazy("change_me"), data=form, follow=True)
        usuario_valido.refresh_from_db()
        assert usuario_valido.genero == form["genero"]


@pytest.mark.django_db
class TestListUsersView:

    def test_quando_o_usuario_nao_fornecer_o_format_um_template_devera_ser_retornado(
        self, client_logado
    ):
        response = client_logado.get(reverse_lazy("users"))
        assert "text/html" in response.headers["Content-Type"]

    def test_quando_o_usuario_fornecer_o_format_como_json_um_json_devera_ser_retornado(
        self, client_logado
    ):
        response = client_logado.get(reverse_lazy("users"), data={"f": "json"})
        assert "application/json" in response.headers["Content-Type"]
        assert len(response.json()["data"]) == 11


@pytest.mark.django_db
class TestChangeUserView:

    def test_quando_o_formulario_for_valido_o_usuario_deve_ser_atualizado(
        self, usuario_valido, factory_data_fake, grupo_usuario, client_logado
    ):
        form = {
            "nome": factory_data_fake.name(),
            "email": factory_data_fake.email(),
            "telefone": "65999999999",
            "password": "test",
            "groups": grupo_usuario.id,
            "genero": "M",
        }
        response = client_logado.post(
            reverse_lazy("user-edit", kwargs={"pk": usuario_valido.id}),
            data=form,
            follow=True,
        )
        usuario_valido.refresh_from_db()
        assert usuario_valido.nome == form["nome"]

    def test_quando_o_formulario_for_invalido_o_usuario_nao_devera_ser_atualizado(
        self, usuario_valido, client_logado
    ):
        form = {"nome": "forcei o erro"}
        response = client_logado.post(
            reverse_lazy("user-edit", kwargs={"pk": usuario_valido.id}),
            data=form,
            follow=True,
        )
        usuario_valido.refresh_from_db()
        assert usuario_valido.nome != form["nome"]


class TestCreateUserView:

    def test_quando_o_formulario_for_valido_o_usuario_deve_ser_criado(
        self, client_logado, grupo_usuario
    ):
        user = baker.prepare(User, cpf="49788189075")
        form_valido = {
            "nome": user.nome,
            "cpf": user.cpf,
            "email": user.email,
            "telefone": user.telefone,
            "password": "test",
            "genero": user.genero,
            "groups": grupo_usuario.id,
        }
        
        response = client_logado.post(reverse_lazy("user-new"), data=form_valido)
        assert User.objects.filter(cpf=form_valido["cpf"]).exists()

    def test_quando_o_formulario_for_invalido_o_usuario_nao_devera_ser_criado(
        self, client_logado
    ):
        form_invalido = {"cpf": "test_invalido", "email": "test@test.com"}
        response = client_logado.post(reverse_lazy("user-new"), data=form_invalido)
        assert not User.objects.filter(cpf=form_invalido["cpf"]).exists()
