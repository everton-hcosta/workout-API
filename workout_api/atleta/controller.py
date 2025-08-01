from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.future import select

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_nome} não foi encontrada.",
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento} não foi encontrado.",
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.now(timezone.utc), **atleta_in.model_dump()
        )

        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar o atleta. Verifique os dados e tente novamente.",
        )

    return atleta_out


@router.get(
    path="/",
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: str | None = Query(default=None, description="Filtrar pelo nome"),
    cpf: str | None = Query(default=None, description="Filtrar pelo CPF"),
    limit: int = Query(default=100, ge=1, le=1000, description="Limite de resultados"),
    offset: int = Query(default=0, ge=0, description="Deslocamento para paginação"),
) -> list[AtletaOut]:
    stmt = select(AtletaModel)

    if nome:
        stmt = stmt.where(func.unaccent(AtletaModel.nome).ilike(f"%{nome}%"))
    if cpf:
        cpf = cpf.replace(".", "").replace("-", "")
        stmt = stmt.where(AtletaModel.cpf.ilike(f"%{cpf}%"))

    stmt = stmt.offset(offset).limit(limit).order_by(AtletaModel.nome)

    result = await db_session.execute(stmt)
    atletas = result.scalars().all()

    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum atleta encontrado.",
        )

    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.get(
    path="/{id}",
    summary="Consultar um atleta pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(
    id: UUID4,
    db_session: DatabaseDependency,
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com ID {id} não encontrada.",
        )

    return atleta


@router.patch(
    path="/{id}",
    summary="Editar um atleta pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(
    id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com ID {id} não encontrada.",
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)

    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    path="/{id}",
    summary="Excluir um atleta pelo ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(
    id: UUID4,
    db_session: DatabaseDependency,
) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com ID {id} não encontrada.",
        )

    await db_session.delete(atleta)
    await db_session.commit()
