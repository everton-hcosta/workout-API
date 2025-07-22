from typing import Annotated

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
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
