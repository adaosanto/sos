import pytest
from model_bakery import baker

from ..backends import CustomAuthBackend
from ..models import Vitima


@pytest.fixture
def backend():
    backend = CustomAuthBackend()
    return backend


@pytest.fixture
def vitima_existente(db):
    user = baker.make("Vitima")
    user.save()

    return user


@pytest.mark.django_db
class TestCustomAuthBackend:
    def test_deve_retorna_uma_vitima_quando_for_fornecido_cpf_e_senhas_correta(
        self, vitima_existente, backend: CustomAuthBackend
    ):
        vitima_retornada = backend.authenticate(
            request=None, cpf=vitima_existente.cpf, password=vitima_existente.chave_acesso
        )
        assert vitima_retornada == vitima_existente

    @pytest.mark.django_db
    def test_deve_retorna_none_quando_vitima_com_senha_incorreta(
        self, backend: CustomAuthBackend
    ):
        vitima_retornada = backend.authenticate(request=None, cpf=None, password=None)
        assert vitima_retornada is None
