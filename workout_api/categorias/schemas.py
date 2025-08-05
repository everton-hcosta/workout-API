from typing import Annotated

from pydantic import UUID4, ConfigDict, Field

from workout_api.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    model_config = ConfigDict(from_attributes=True)
    nome: Annotated[
        str, Field(description="Nome da categoria", example="Scale", max_length=50)
    ]


class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]
<<<<<<< HEAD
=======


class CategoriaAtleta(CategoriaIn):
    nome: Annotated[str, Field(description="nome da categoria")]


class CategoriaUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
        Field(None, description="Nome da categoria", example="Scale", max_length=10),
    ]
>>>>>>> b37bbe4 (:construction: Adiciona suporte à paginação nas rotas de atletas, categorias e centros de treinamento, removendo a implementação anterior de resposta paginada.)
