from uuid import uuid4

<<<<<<< HEAD
from fastapi import APIRouter, Body, HTTPException, status
=======
from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
>>>>>>> b37bbe4 (:construction: Adiciona suporte à paginação nas rotas de atletas, categorias e centros de treinamento, removendo a implementação anterior de resposta paginada.)
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:

    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
    path="/",
    summary="Consultar todas as categorias",
    status_code=status.HTTP_200_OK,
<<<<<<< HEAD
    response_model=list[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency,
) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (
        (await db_session.execute(select(CategoriaModel))).scalars().all()
    )

    return categorias

=======
    response_model=Page[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency,
    offset: int = Query(0, ge=0, description="Posição inicial (offset)"),
    limit: int = Query(50, ge=1, le=100, description="Limite de itens por página"),
    nome: str | None = Query(default=None, description="Filtrar pelo nome"),
) -> Page[CategoriaOut]:
    stmt = select(CategoriaModel).order_by(CategoriaModel.nome)

    if nome:
        stmt = stmt.where(
            func.unaccent(CategoriaModel.nome).ilike(func.unaccent(f"%{nome}%"))
        )

    categorias = await sqlalchemy_paginate(
        db_session, stmt, params=Params(offset=offset, limit=limit)
    )

    if not categorias.items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma categoria encontrado.",
        )

    return categorias


# Adicione a paginação
add_pagination(router)

>>>>>>> b37bbe4 (:construction: Adiciona suporte à paginação nas rotas de atletas, categorias e centros de treinamento, removendo a implementação anterior de resposta paginada.)

@router.get(
    path="/{id}",
    summary="Consultar uma categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(
    id: UUID4,
    db_session: DatabaseDependency,
) -> CategoriaOut:
    categoria: CategoriaOut = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {id} não encontrada.",
        )

    return categoria
