"""Rename existing property_card table

Revision ID: 8f60a888c179
Revises: 2c1d50b5cfa6
Create Date: 2022-04-05 16:44:52.441832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f60a888c179'
down_revision = '2c1d50b5cfa6'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('property_card', 'property_card_old')


def downgrade():
    op.rename_table('property_card_old', 'property_card')
