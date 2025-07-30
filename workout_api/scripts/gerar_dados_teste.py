# scripts/popular_atletas.py

import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from faker import Faker
from faker.providers import BaseProvider

from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.configs.database import get_session


class ProvedorLimitador(BaseProvider):
    def limitador(self, nome_campo: str, tamanho_maximo: int) -> str:
        """
        Gera um valor do campo `nome_campo` (ex: 'name', 'unique.word')
        com no máximo `tamanho_maximo` caracteres.
        """
        # Suporte a campos aninhados como 'unique.word' ou 'random_element'
        partes = nome_campo.split(".")
        gerador = self.generator
        for parte in partes:
            if not hasattr(gerador, parte):
                raise ValueError(f"O campo '{nome_campo}' é inválido.")
            gerador = getattr(gerador, parte)

        # Gera o valor e ajusta quebras de linha
        valor = str(gerador()).replace("\n", ", ")

        if len(valor) <= tamanho_maximo:
            return valor

        return valor[:tamanho_maximo].rsplit(" ", 1)[0]


fake = Faker("pt_BR")
fake.add_provider(ProvedorLimitador)

NUM_ATLETAS = 1000
NUM_CATEGORIAS = 10
NUM_CTS = 10


async def main():
    async for session in get_session():
        # Criar categorias
        categorias = []
        for _ in range(NUM_CATEGORIAS):
            nome_categoria = fake.limitador("unique.word").capitalize()
            categoria = CategoriaModel(nome=nome_categoria)
            session.add(categoria)
            categorias.append(categoria)

        # Criar centros de treinamento
        centros = []
        for _ in range(NUM_CTS):
            nome_ct = f"CT {fake.limitador('unique.last_name').capitalize()}"
            endereco = fake.address().replace("\n", ", ")
            proprietario = fake.name()
            centro = CentroTreinamentoModel(
                nome=nome_ct, endereco=endereco, proprietario=proprietario
            )
            session.add(centro)
            centros.append(centro)

        await session.flush()  # garante que ids sejam gerados

        # Criar atletas
        for _ in range(NUM_ATLETAS):
            nome = fake.name()
            cpf = fake.unique.ssn().replace(".", "").replace("-", "")
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
