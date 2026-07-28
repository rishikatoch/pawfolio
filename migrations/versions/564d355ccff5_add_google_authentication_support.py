"""Add Google authentication support

Revision ID: 564d355ccff5
Revises: 38eb66f32967
Create Date: 2026-07-28

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "564d355ccff5"
down_revision = "38eb66f32967"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user") as batch_op:

        batch_op.add_column(
            sa.Column(
                "google_id",
                sa.String(length=255),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "auth_provider",
                sa.String(length=20),
                nullable=False,
                server_default="local",
            )
        )

        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=True,
        )

        batch_op.create_unique_constraint(
            "uq_user_google_id",
            ["google_id"],
        )

    op.execute(
        "UPDATE \"user\" SET auth_provider='local' " "WHERE auth_provider IS NULL"
    )

    with op.batch_alter_table("user") as batch_op:

        batch_op.alter_column(
            "auth_provider",
            server_default=None,
        )


def downgrade():
    with op.batch_alter_table("user") as batch_op:

        batch_op.drop_constraint(
            "uq_user_google_id",
            type_="unique",
        )

        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=False,
        )

        batch_op.drop_column("auth_provider")

        batch_op.drop_column("google_id")
