"""Add contact_email column to photo_gallery table

Revision ID: 0fd686afb6d5
Revises: 0f114a99e5cf
Create Date: 2022-04-06 15:13:04.315459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0fd686afb6d5'
down_revision = '0f114a99e5cf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('photo_gallery', sa.Column('contact_email', sa.String(length=256), nullable=True))
    op.add_column('tax_photo', sa.Column('contact_email', sa.String(length=256), nullable=True))


def downgrade():
    op.drop_column('photo_gallery', 'contact_email')
    op.drop_column('tax_photo', 'contact_email')
