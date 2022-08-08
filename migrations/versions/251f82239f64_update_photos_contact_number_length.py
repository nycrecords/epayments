"""Update photos contact_number length

Revision ID: 251f82239f64
Revises: d935da7400dd
Create Date: 2022-08-05 18:37:13.037400

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '251f82239f64'
down_revision = 'd935da7400dd'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('photo_gallery', 'contact_number',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=64),
               existing_nullable=True)
    op.alter_column('tax_photo', 'contact_number',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=64),
               existing_nullable=True)


def downgrade():
    op.alter_column('tax_photo', 'contact_number',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
    op.alter_column('photo_gallery', 'contact_number',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
