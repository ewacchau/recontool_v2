"""init schema

Revision ID: 0001
Revises: 
Create Date: 2025-09-08 20:45:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'scan_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.Column('target', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('scan_runs')

