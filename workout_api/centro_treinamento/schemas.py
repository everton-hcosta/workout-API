from typing import Annotated

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
