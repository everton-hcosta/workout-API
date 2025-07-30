"""Adiciona timezone ao campo created_at

Revision ID: 96af2c735a11
Revises: 4aaea466cd0e
Create Date: 2025-07-29 05:01:03.537983

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96af2c735a11"
down_revision: Union[str, Sequence[str], None] = "4aaea466cd0e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "atletas",  # nome da tabela
        "created_at",  # nome da coluna
        type_=sa.DateTime(timezone=True),  # novo tipo com timezone
        postgresql_using="created_at AT TIME ZONE 'UTC'",  # converte valor atual
    )


def downgrade():
    op.alter_column(
        "atletas",
        "created_at",
        type_=sa.DateTime(timezone=False),  # volta para o tipo anterior
        postgresql_using="created_at",
    )
