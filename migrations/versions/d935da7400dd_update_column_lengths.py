"""Update photo_gallery image_id length

Revision ID: d935da7400dd
Revises: 66b7626d3457
Create Date: 2022-05-23 13:36:23.378436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd935da7400dd'
down_revision = '66b7626d3457'
branch_labels = None
depends_on = Nonew


def upgrade():
    op.alter_column('birth_cert', 'father_name',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=105),
               existing_nullable=True)
    op.alter_column('birth_cert', 'mother_name',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=105),
               existing_nullable=True)
    op.alter_column('birth_search', 'father_name',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=105),
               existing_nullable=True)
    op.alter_column('birth_search', 'mother_name',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=105),
               existing_nullable=True)
    op.alter_column('photo_gallery', 'image_id',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=35),
               existing_nullable=False)


def downgrade():
    op.alter_column('photo_gallery', 'image_id',
               existing_type=sa.String(length=35),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    op.alter_column('birth_search', 'mother_name',
               existing_type=sa.String(length=105),
               type_=sa.VARCHAR(length=40),
               existing_nullable=True)
    op.alter_column('birth_search', 'father_name',
               existing_type=sa.String(length=105),
               type_=sa.VARCHAR(length=40),
               existing_nullable=True)
    op.alter_column('birth_cert', 'mother_name',
               existing_type=sa.String(length=105),
               type_=sa.VARCHAR(length=40),
               existing_nullable=True)
    op.alter_column('birth_cert', 'father_name',
               existing_type=sa.String(length=105),
               type_=sa.VARCHAR(length=40),
               existing_nullable=True)
