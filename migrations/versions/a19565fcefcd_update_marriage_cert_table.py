"""Update marriage_cert table

Revision ID: a19565fcefcd
Revises: 6ca06ecb65c0
Create Date: 2022-04-15 12:35:23.959313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a19565fcefcd'
down_revision = '6ca06ecb65c0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('marriage_cert', sa.Column('bride_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_cert', sa.Column('alt_bride_last_name', sa.String(length=25), nullable=True))
    op.add_column('marriage_cert', sa.Column('alt_bride_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_cert', sa.Column('alt_bride_first_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_cert', sa.Column('groom_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_cert', sa.Column('alt_groom_last_name', sa.String(length=25), nullable=True))
    op.add_column('marriage_cert', sa.Column('alt_groom_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_cert', sa.Column('alt_groom_first_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_cert', sa.Column('exemplification_copies', sa.String(length=1), nullable=True))
    op.add_column('marriage_cert', sa.Column('raised_seal', sa.Boolean(), nullable=False))
    op.add_column('marriage_cert', sa.Column('raised_seal_copies', sa.String(length=1), nullable=True))
    op.add_column('marriage_cert', sa.Column('no_amends', sa.Boolean(), nullable=False))
    op.add_column('marriage_cert', sa.Column('no_amends_copies', sa.String(length=1), nullable=True))
    op.alter_column('marriage_cert', 'letter', nullable=True, new_column_name='exemplification')


def downgrade():
    op.alter_column('marriage_cert', 'exemplification', nullable=True, new_column_name='letter')
    op.drop_column('marriage_cert', 'no_amends_copies')
    op.drop_column('marriage_cert', 'no_amends')
    op.drop_column('marriage_cert', 'raised_seal_copies')
    op.drop_column('marriage_cert', 'raised_seal')
    op.drop_column('marriage_cert', 'exemplification_copies')
    op.drop_column('marriage_cert', 'alt_groom_first_name')
    op.drop_column('marriage_cert', 'alt_groom_middle_name')
    op.drop_column('marriage_cert', 'alt_groom_last_name')
    op.drop_column('marriage_cert', 'groom_middle_name')
    op.drop_column('marriage_cert', 'alt_bride_first_name')
    op.drop_column('marriage_cert', 'alt_bride_middle_name')
    op.drop_column('marriage_cert', 'alt_bride_last_name')
    op.drop_column('marriage_cert', 'bride_middle_name')
