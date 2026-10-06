"""add professional activation fields

Revision ID: 0004_add_professional_activation
Revises: 0003_add_professional_auth
Create Date: 2026-09-28
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_add_professional_activation"
down_revision: Union[str, Sequence[str], None] = (
    "0003_add_professional_auth"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "professionals",
        sa.Column(
            "activation_token_hash",
            sa.String(length=64),
            nullable=True,
        ),
    )

    op.add_column(
        "professionals",
        sa.Column(
            "activation_token_created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "professionals",
        sa.Column(
            "activation_token_expires_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_professionals_activation_token_hash",
        "professionals",
        ["activation_token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_professionals_activation_token_hash",
        table_name="professionals",
    )

    op.drop_column(
        "professionals",
        "activation_token_expires_at",
    )

    op.drop_column(
        "professionals",
        "activation_token_created_at",
    )

    op.drop_column(
        "professionals",
        "activation_token_hash",
    )