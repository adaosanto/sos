import uuid

import pytest
from model_bakery import baker

from ..models import User, get_file_path


@pytest.fixture
def filename():
    return f"{uuid.uuid4()}.png"


@pytest.fixture
def usuario(db):
    return baker.make(User)


@pytest.mark.django_db
class TestGetFilePath:
    def test_get_file_path(self, filename):
        arquivo = get_file_path(None, "foto.png")
        assert len(arquivo) == len(filename)


@pytest.mark.django_db
class TestUser:
    def test_quando_chamar_a_funcao_get_full_name_deve_retorna_o_nome(self, usuario):
        usuario.get_full_name() == usuario.nome

    def test_quando_chamar_a_funcao_get_short_name_name_deve_retorna_o_nome(
        self, usuario
    ):
        usuario.get_short_name() == usuario.nome
