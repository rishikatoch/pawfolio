"""Add notification preferences to user

Revision ID: b15a9441aca1
Revises: fc25d8518262
Create Date: 2026-07-28 22:34:09.466359
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b15a9441aca1"
down_revision = "fc25d8518262"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "email_notifications",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            )
        )

        batch_op.add_column(
            sa.Column(
                "reminder_days",
                sa.Integer(),
                nullable=False,
                server_default=sa.text("7"),
            )
        )

        batch_op.add_column(
            sa.Column(
                "notification_time",
                sa.Time(),
                nullable=False,
                server_default=sa.text("'09:00:00'"),
            )
        )

        batch_op.add_column(
            sa.Column(
                "timezone",
                sa.String(length=50),
                nullable=False,
                server_default=sa.text("'Asia/Kolkata'"),
            )
        )

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "email_notifications",
            server_default=None,
        )

        batch_op.alter_column(
            "reminder_days",
            server_default=None,
        )

        batch_op.alter_column(
            "notification_time",
            server_default=None,
        )

        batch_op.alter_column(
            "timezone",
            server_default=None,
        )


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("timezone")
        batch_op.drop_column("notification_time")
        batch_op.drop_column("reminder_days")
        batch_op.drop_column("email_notifications")
