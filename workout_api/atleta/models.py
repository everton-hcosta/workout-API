from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workout_api.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atletas"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # adiciona suporte a timezone
        nullable=False,
        default=lambda: datetime.now(timezone.utc),  # valor timezone-aware
    )
    categoria: Mapped["CategoriaModel"] = relationship(
        back_populates="atleta", lazy="selectin"
    )
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.pk_id"))
    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(
        back_populates="atleta", lazy="selectin"
    )
    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey("centros_treinamento.pk_id")
    )
