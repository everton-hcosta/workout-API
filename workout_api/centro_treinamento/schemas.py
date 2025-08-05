from typing import Annotated, Optional

from pydantic import UUID4, ConfigDict, Field

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT King",
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Enderço do centro de treinamento",
            example="Rua X, Q01",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description="Proprietário centro de treinamento",
            example="Kreber",
            max_length=30,
        ),
    ]


class CentroTreinamentoAtleta(BaseSchema):
    model_config = ConfigDict(from_attributes=True)
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT King",
            max_length=20,
        ),
    ]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="Identificador da centro do treinamento")]
<<<<<<< HEAD
=======


class CentroTreinamentoUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
        Field(
            None,
            description="Nome do centro de treinamento",
            example="CT Crown",
            max_length=20,
        ),
    ]
    endereco: Annotated[
        Optional[str],
        Field(
            None,
            description="Endereço do centro de treinamento",
            example="Rua X, Q01",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        Optional[str],
        Field(
            None, description="Nome do proprietário", example="Craudio", max_length=30
        ),
    ]
>>>>>>> b37bbe4 (:construction: Adiciona suporte à paginação nas rotas de atletas, categorias e centros de treinamento, removendo a implementação anterior de resposta paginada.)
