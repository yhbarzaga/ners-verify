"""Initial database tables

Revision ID: c684fcc2d488
Revises: 
Create Date: 2024-02-14 16:42:13.376396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c684fcc2d488"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "documents_type",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
    )
    op.create_table(
        "staff",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column(
            "internal_id",
            sa.String(),
            nullable=False,
            comment="Stand for the unique identifier of the user inside the ERP",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("internal_id"),
    )

    op.create_index(
        op.f("ix_staff_internal_id"), "staff", ["internal_id"], unique=False
    )

    op.create_table(
        "documents",
        sa.Column("uid", sa.UUID(), nullable=False),
        sa.Column(
            "total",
            sa.DECIMAL(precision=7, scale=2),
            nullable=True,
            comment="Total to be refunded",
        ),
        sa.Column("staff_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["staff_id"],
            ["staff.uid"],
        ),
        sa.PrimaryKeyConstraint("uid"),
    )


def downgrade():
    op.drop_table("documents")

    op.drop_index(op.f("ix_staff_internal_id"), table_name="staff")
    op.drop_table("staff")

    op.drop_table("documents_type")
