from fastapi import APIRouter

from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categoria

api_router = APIRouter()

api_router.include_router(atleta, prefix="/atleta", tags=["atleta"])
api_router.include_router(categoria, prefix="/categoria", tags=["categoria"])
