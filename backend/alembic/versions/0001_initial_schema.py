from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.create_index(
        "ix_categories_name",
        "categories",
        ["name"],
        unique=True,
    )

    op.create_index(
        "ix_categories_slug",
        "categories",
        ["slug"],
        unique=True,
    )

    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column(
            "locality",
            sa.String(120),
            nullable=False,
            server_default="Resistencia",
        ),
        sa.Column(
            "province",
            sa.String(120),
            nullable=False,
            server_default="Chaco",
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.create_index(
        "ix_locations_name",
        "locations",
        ["name"],
        unique=True,
    )

    op.create_table(
        "professionals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(30), nullable=False),
        sa.Column("whatsapp", sa.String(30)),
        sa.Column("description", sa.Text()),
        sa.Column("years_experience", sa.Integer()),
        sa.Column("instagram", sa.String(150)),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "identity_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_index(
        "ix_professionals_phone",
        "professionals",
        ["phone"],
        unique=True,
    )

    op.create_table(
        "professional_categories",
        sa.Column(
            "professional_id",
            sa.Integer(),
            sa.ForeignKey(
                "professionals.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        ),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey(
                "categories.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        ),
    )

    op.create_table(
        "professional_locations",
        sa.Column(
            "professional_id",
            sa.Integer(),
            sa.ForeignKey(
                "professionals.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        ),
        sa.Column(
            "location_id",
            sa.Integer(),
            sa.ForeignKey(
                "locations.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        ),
    )

    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "professional_id",
            sa.Integer(),
            sa.ForeignKey(
                "professionals.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(150),
            nullable=False,
        ),
        sa.Column("description", sa.Text()),
        sa.Column(
            "status",
            sa.String(30),
            nullable=False,
            server_default="completed",
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
        ),
    )

    op.create_index(
        "ix_jobs_professional_id",
        "jobs",
        ["professional_id"],
    )

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "professional_id",
            sa.Integer(),
            sa.ForeignKey(
                "professionals.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "job_id",
            sa.Integer(),
            sa.ForeignKey(
                "jobs.id",
                ondelete="SET NULL",
            ),
            unique=True,
        ),
        sa.Column(
            "rating",
            sa.SmallInteger(),
            nullable=False,
        ),
        sa.Column("comment", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="ck_reviews_rating",
        ),
    )

    op.create_index(
        "ix_reviews_professional_id",
        "reviews",
        ["professional_id"],
    )

    op.create_table(
        "verifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "professional_id",
            sa.Integer(),
            sa.ForeignKey(
                "professionals.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(30),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("method", sa.String(50)),
        sa.Column("notes", sa.Text()),
        sa.Column(
            "verified_at",
            sa.DateTime(timezone=True),
        ),
    )

    op.create_unique_constraint(
        "uq_verifications_professional_id",
        "verifications",
        ["professional_id"],
    )


def downgrade():
    op.drop_table("verifications")
    op.drop_index(
        "ix_reviews_professional_id",
        table_name="reviews",
    )
    op.drop_table("reviews")
    op.drop_index(
        "ix_jobs_professional_id",
        table_name="jobs",
    )
    op.drop_table("jobs")
    op.drop_table("professional_locations")
    op.drop_table("professional_categories")
    op.drop_index(
        "ix_professionals_phone",
        table_name="professionals",
    )
    op.drop_table("professionals")
    op.drop_index(
        "ix_locations_name",
        table_name="locations",
    )
    op.drop_table("locations")
    op.drop_index(
        "ix_categories_slug",
        table_name="categories",
    )
    op.drop_index(
        "ix_categories_name",
        table_name="categories",
    )
    op.drop_table("categories")