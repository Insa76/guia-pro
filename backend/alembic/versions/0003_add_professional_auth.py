"""add professional authentication

Revision ID: 0003_add_professional_auth
Revises: 0002_add_review_token_to_jobs
Create Date: 2026-09-27
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_add_professional_auth"
down_revision = "0002_add_review_token_to_jobs"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "professionals",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "professionals",
        sa.Column(
            "account_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.alter_column(
        "professionals",
        "account_enabled",
        server_default=None,
    )


def downgrade() -> None:

    op.drop_column(
        "professionals",
        "account_enabled",
    )

    op.drop_column(
        "professionals",
        "password_hash",
    )