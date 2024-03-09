import uuid

import pytest
from model_bakery import baker

from vitimas.models import get_file_path


@pytest.fixture
def filename():
    return f"{uuid.uuid4()}.png"


@pytest.mark.django_db
class TestGetFilePath:
    def test_get_file_path(self, filename):
        arquivo = get_file_path(None, "foto.png")
        assert len(arquivo) == len(filename)


@pytest.mark.django_db
class TestSignal:
    @pytest.fixture
    def user_active(self):
        return baker.make("Vitima")

    @pytest.fixture
    def user_inactive(self):
        return baker.make("Vitima", is_active=False)

    def test_status_flag_deve_esta_ativo(self, user_active):
        assert "green" in user_active.status_flag

    def test_status_flag_deve_esta_inativo(self, user_inactive):
        assert "red" in user_inactive.status_flag

    def test_a_conversao_de_str_da_vitima_deve_ser_o_cpf(self, user_active):
        assert str(user_active) == user_active.cpf
