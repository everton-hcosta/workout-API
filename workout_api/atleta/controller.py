from fastapi import APIRouter, Body, status

from workout_api.atleta.schemas import AtletaIn
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_description="Atleta criado com sucesso",
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    pass
