"""Create no_amends table

Revision ID: 6ca06ecb65c0
Revises: 497a8987f92b
Create Date: 2022-04-14 15:39:20.976552

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6ca06ecb65c0'
down_revision = '497a8987f92b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('no_amends',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('num_copies', sa.String(length=1), nullable=False),
                    sa.Column('filename', sa.String(length=256), nullable=False),
                    sa.Column('delivery_method',
                              postgresql.ENUM('mail', 'email', 'pickup', name='delivery_method', create_type=False),
                              nullable=False),
                    sa.Column('suborder_number', sa.String(length=32), nullable=False),
                    sa.ForeignKeyConstraint(['suborder_number'], ['suborders.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('no_amends')
