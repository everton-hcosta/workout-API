import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from faker import Faker
from faker.providers import BaseProvider

from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.configs.database import get_session


class ProvedorDeCampoLimitado(BaseProvider):
    def limitador(self, nome_do_campo: str, tamanho_maximo: int):
        """
        Gera um valor para o campo `nome_do_campo` com no máximo `tamanho_maximo` caracteres.
        """
        # Garante que o campo exista no Faker
        if not hasattr(self.generator, nome_do_campo):
            raise ValueError(f"'{nome_do_campo}' não é um campo válido do Faker.")

        # Chama o método correspondente do campo
        valor_bruto = getattr(self.generator, nome_do_campo)()

        # Substitui quebras de linha por vírgula e espaço
        valor = str(valor_bruto).replace("\n", ", ")

        if len(valor) <= tamanho_maximo:
            return valor

        # Tenta cortar no último espaço antes do limite
        return valor[:tamanho_maximo].rsplit(" ", 1)[0]


fake = Faker("pt_BR")
fake.add_provider(ProvedorDeCampoLimitado)

NUM_ATLETAS = 1000
NUM_CATEGORIAS = 10
NUM_CTS = 10


async def main():
    async for session in get_session():
        # Criar categorias
        categorias = []
        for _ in range(NUM_CATEGORIAS):
            nome_categoria = fake.unique.limitador("word", 50).capitalize()
            categoria = CategoriaModel(nome=nome_categoria)
            session.add(categoria)
            categorias.append(categoria)

        # Criar centros de treinamento
        centros = []
        for _ in range(NUM_CTS):
            nome_ct = f"CT {fake.unique.limitador("last_name", 50).capitalize()}"
            endereco = fake.limitador("address", 60).replace("\n", ", ")
            proprietario = fake.limitador("name", 30).capitalize()
            centro = CentroTreinamentoModel(
                nome=nome_ct, endereco=endereco, proprietario=proprietario
            )
            session.add(centro)
            centros.append(centro)

        await session.flush()  # garante que ids sejam gerados

        # Criar atletas
        for _ in range(NUM_ATLETAS):
            nome = fake.limitador("name", 50).capitalize()
            cpf = fake.unique.limitador("ssn", 11).replace(".", "").replace("-", "")
            idade = fake.random_int(min=15, max=90)
            peso = round(fake.random_number(digits=2) + fake.random.random(), 1)
            altura = round(fake.random.uniform(1.50, 2.00), 2)
            sexo = fake.random_element(elements=("M", "F"))

            categoria = fake.random_element(elements=categorias)
            centro = fake.random_element(elements=centros)

            atleta = AtletaModel(
                id=uuid4(),
                nome=nome,
                cpf=cpf,
                idade=idade,
                peso=peso,
                altura=altura,
                sexo=sexo,
                created_at=datetime.now(timezone.utc),
                categoria_id=categoria.pk_id,
                centro_treinamento_id=centro.pk_id,
            )
            session.add(atleta)

        await session.commit()
        print(f"✅ {NUM_ATLETAS} atletas criados com sucesso.")
        print(f"📦 {NUM_CATEGORIAS} categorias e {NUM_CTS} CTs adicionados.")


if __name__ == "__main__":
    asyncio.run(main())
