"""add review token to jobs

Revision ID: 0002_add_review_token_to_jobs
Revises: 0001_initial_schema
Create Date: 2026-09-24
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_review_token_to_jobs"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "jobs",
        sa.Column(
            "review_token_hash",
            sa.String(length=64),
            nullable=True,
        ),
    )

    op.add_column(
        "jobs",
        sa.Column(
            "review_token_created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.create_unique_constraint(
        "uq_jobs_review_token_hash",
        "jobs",
        ["review_token_hash"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_jobs_review_token_hash",
        "jobs",
        type_="unique",
    )

    op.drop_column(
        "jobs",
        "review_token_created_at",
    )

    op.drop_column(
        "jobs",
        "review_token_hash",
    )