from typing import Annotated

from pydantic import Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema, OutMixIn


class Atleta(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do atleta", example="João Silva", max_length=50)
    ]
    cpf: Annotated[
        str, Field(description="CPF do atleta", example="12345678910", max_length=11)
    ]
    idade: Annotated[int, Field(description="Idade do atleta", example="30")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example="80.1")]
    altura: Annotated[
        PositiveFloat, Field(description="Altura do atleta", example="1.77")
    ]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixIn):
    pass
