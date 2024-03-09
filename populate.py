from vitimas.models import Vitima

from faker import Faker
from model_bakery import baker
factory_data = Faker('pt_BR')

for _ in range(0,10):
    baker.make(Vitima, cpf=factory_data.cpf(), nome=factory_data.name_female(), rg=factory_data.rg(), endereco=factory_data.address(), telefone=factory_data.phone_number(), suspeito=factory_data.name())