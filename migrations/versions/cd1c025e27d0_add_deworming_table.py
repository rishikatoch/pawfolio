"""Add deworming table

Revision ID: cd1c025e27d0
Revises: 8bbe4b571862
Create Date: 2026-07-24 13:40:13.373259

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "cd1c025e27d0"
down_revision = "8bbe4b571862"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "deworming",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "pet_id",
            sa.Integer(),
            sa.ForeignKey("pet.id"),
            nullable=False,
        ),
        sa.Column(
            "medicine_name",
            sa.String(100),
            nullable=False,
        ),
        sa.Column(
            "date_given",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "next_due",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
        ),
        sa.Column(
            "veterinarian",
            sa.String(100),
        ),
    )


def downgrade():

    op.drop_table("deworming")
