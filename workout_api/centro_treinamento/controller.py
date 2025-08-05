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

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(), **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
    path="/",
    summary="Consultar todos centros de treinamento",
    status_code=status.HTTP_200_OK,
<<<<<<< HEAD
    response_model=list[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency,
) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (
        (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    )
=======
    response_model=Page[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency,
    offset: int = Query(0, ge=0, description="Posição inicial (offset)"),
    limit: int = Query(50, ge=1, le=100, description="Limite de itens por página"),
    nome: str | None = Query(default=None, description="Filtrar pelo nome"),
) -> Page[CentroTreinamentoOut]:
    stmt = select(CentroTreinamentoModel).order_by(CentroTreinamentoModel.nome)

    if nome:
        stmt = stmt.where(
            func.unaccent(CentroTreinamentoModel.nome).ilike(func.unaccent(f"%{nome}%"))
        )

    centros_treinamento = await sqlalchemy_paginate(
        db_session, stmt, params=Params(offset=offset, limit=limit)
    )

    if not centros_treinamento.items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum centro de treinamento encontrado.",
        )

    return centros_treinamento


# Adicione a paginação
add_pagination(router)
>>>>>>> b37bbe4 (:construction: Adiciona suporte à paginação nas rotas de atletas, categorias e centros de treinamento, removendo a implementação anterior de resposta paginada.)

    return centros_treinamento


@router.get(
    path="/{id}",
    summary="Consultar um centro de treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(
    id: UUID4,
    db_session: DatabaseDependency,
) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not centro_treinamento_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento com ID {id} não encontrada.",
        )

    return centro_treinamento_out
