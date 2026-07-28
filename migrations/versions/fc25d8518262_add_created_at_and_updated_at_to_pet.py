"""Add created_at and updated_at to pet

Revision ID: fc25d8518262
Revises: 564d355ccff5
Create Date: 2026-07-28 16:21:07.141938
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fc25d8518262"
down_revision = "564d355ccff5"
branch_labels = None
depends_on = None


def upgrade():
    # -----------------------------
    # Deworming
    # -----------------------------
    with op.batch_alter_table("deworming", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.create_index(
            batch_op.f("ix_deworming_pet_id"),
            ["pet_id"],
            unique=False,
        )

    # -----------------------------
    # Pet
    # -----------------------------
    with op.batch_alter_table("pet", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.alter_column(
            "user_id",
            existing_type=sa.INTEGER(),
            nullable=False,
        )

    # -----------------------------
    # User
    # -----------------------------
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=postgresql.TIMESTAMP(),
            nullable=False,
            existing_server_default=sa.text("now()"),
        )

        batch_op.drop_constraint(
            batch_op.f("user_email_key"),
            type_="unique",
        )

        batch_op.create_index(
            batch_op.f("ix_user_email"),
            ["email"],
            unique=True,
        )

    # -----------------------------
    # Vaccination
    # -----------------------------
    with op.batch_alter_table("vaccination", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.create_index(
            batch_op.f("ix_vaccination_pet_id"),
            ["pet_id"],
            unique=False,
        )

    # -----------------------------
    # Vet Visit
    # -----------------------------
    with op.batch_alter_table("vet_visit", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.create_index(
            batch_op.f("ix_vet_visit_pet_id"),
            ["pet_id"],
            unique=False,
        )


def downgrade():
    # -----------------------------
    # Vet Visit
    # -----------------------------
    with op.batch_alter_table("vet_visit", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_vet_visit_pet_id"))
        batch_op.drop_column("updated_at")

    # -----------------------------
    # Vaccination
    # -----------------------------
    with op.batch_alter_table("vaccination", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_vaccination_pet_id"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    # -----------------------------
    # User
    # -----------------------------
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_user_email"))

        batch_op.create_unique_constraint(
            batch_op.f("user_email_key"),
            ["email"],
            postgresql_nulls_not_distinct=False,
        )

        batch_op.alter_column(
            "created_at",
            existing_type=postgresql.TIMESTAMP(),
            nullable=True,
            existing_server_default=sa.text("now()"),
        )

    # -----------------------------
    # Pet
    # -----------------------------
    with op.batch_alter_table("pet", schema=None) as batch_op:
        batch_op.alter_column(
            "user_id",
            existing_type=sa.INTEGER(),
            nullable=True,
        )

        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    # -----------------------------
    # Deworming
    # -----------------------------
    with op.batch_alter_table("deworming", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_deworming_pet_id"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
