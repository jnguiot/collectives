"""add uploaded_files table

Revision ID: 6b292b7e7d7b
Revises: 0110110fa81e
Create Date: 2022-09-07 08:20:51.518289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "6b292b7e7d7b"
down_revision = "0110110fa81e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "uploaded_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("session_id", sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_uploaded_files_event_id"), "uploaded_files", ["event_id"], unique=False
    )
    op.create_index(
        op.f("ix_uploaded_files_user_id"), "uploaded_files", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("uploaded_files")
    # ### end Alembic commands ###
