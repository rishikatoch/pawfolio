"""Add schedule and age to deworming

Revision ID: cc017dba7367
Revises: cd1c025e27d0
Create Date: 2026-07-24 14:13:36.526541

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "cc017dba7367"
down_revision = "cd1c025e27d0"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("deworming", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "schedule_used",
                sa.String(length=50),
                nullable=False,
                server_default="Manual",
            )
        )

        batch_op.add_column(
            sa.Column(
                "age_at_deworming",
                sa.String(length=50),
                nullable=False,
                server_default="Unknown",
            )
        )

    with op.batch_alter_table("deworming", schema=None) as batch_op:

        batch_op.alter_column(
            "schedule_used",
            server_default=None,
        )

        batch_op.alter_column(
            "age_at_deworming",
            server_default=None,
        )


def downgrade():

    with op.batch_alter_table("deworming", schema=None) as batch_op:

        batch_op.drop_column("age_at_deworming")

        batch_op.drop_column("schedule_used")
