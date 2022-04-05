"""Create new property_card table

Revision ID: 0f114a99e5cf
Revises: 8f60a888c179
Create Date: 2022-04-05 16:45:54.304219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '0f114a99e5cf'
down_revision = '8f60a888c179'
branch_labels = None
depends_on = None

conn = op.get_bind()
inspector = Inspector.from_engine(conn)
tables = inspector.get_table_names()


def upgrade():
    if 'property_card_new' in tables:
        op.rename_table('property_card_new', 'property_card')
    else:
        op.create_table('property_card',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('borough',
                                  postgresql.ENUM('Bronx', 'Manhattan', 'Staten Island', 'Brooklyn', 'Queens',
                                                  name='borough',
                                                  create_type=False), nullable=False),
                        sa.Column('block', sa.String(length=9), nullable=False),
                        sa.Column('lot', sa.String(length=9), nullable=False),
                        sa.Column('building_number', sa.String(length=10), nullable=True),
                        sa.Column('street', sa.String(length=40), nullable=True),
                        sa.Column('num_copies', sa.String(length=1), nullable=False),
                        sa.Column('raised_seal', sa.Boolean(), nullable=False),
                        sa.Column('raised_seal_copies', sa.String(length=1), nullable=True),
                        sa.Column('delivery_method',
                                  postgresql.ENUM('mail', 'email', 'pickup', name='delivery_method', create_type=False),
                                  nullable=False),
                        sa.Column('contact_number', sa.String(length=64), nullable=True),
                        sa.Column('contact_email', sa.String(length=256), nullable=True),
                        sa.Column('suborder_number', sa.String(length=32), nullable=False),
                        sa.ForeignKeyConstraint(['suborder_number'], ['suborders.id'], ),
                        sa.PrimaryKeyConstraint('id')
                        )


def downgrade():
    op.rename_table('property_card', 'property_card_new')
