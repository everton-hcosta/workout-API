from typing import Annotated

from pydantic import UUID4, ConfigDict, Field

from workout_api.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    model_config = ConfigDict(from_attributes=True)
    nome: Annotated[
        str, Field(description="Nome da categoria", example="Scale", max_length=10)
    ]


class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]
