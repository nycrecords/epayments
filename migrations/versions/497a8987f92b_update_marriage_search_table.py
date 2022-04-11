"""Update marriage_search table

Revision ID: 497a8987f92b
Revises: 0fd686afb6d5
Create Date: 2022-04-07 10:14:04.152122

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '497a8987f92b'
down_revision = '0fd686afb6d5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('marriage_search', sa.Column('bride_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_search', sa.Column('alt_bride_last_name', sa.String(length=25), nullable=True))
    op.add_column('marriage_search', sa.Column('alt_bride_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_search', sa.Column('alt_bride_first_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_search', sa.Column('groom_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_search', sa.Column('alt_groom_last_name', sa.String(length=25), nullable=True))
    op.add_column('marriage_search', sa.Column('alt_groom_middle_name', sa.String(length=40), nullable=True))
    op.add_column('marriage_search', sa.Column('alt_groom_first_name', sa.String(length=40), nullable=True))
    op.alter_column('marriage_search', 'letter', nullable=True, new_column_name='exemplification')
    op.add_column('marriage_search', sa.Column('exemplification_copies', sa.String(length=1), nullable=True))
    op.add_column('marriage_search', sa.Column('raised_seal', sa.Boolean(), nullable=False))
    op.add_column('marriage_search', sa.Column('raised_seal_copies', sa.String(length=1), nullable=True))
    op.add_column('marriage_search', sa.Column('no_amends', sa.Boolean(), nullable=False))
    op.add_column('marriage_search', sa.Column('no_amends_copies', sa.String(length=1), nullable=True))


def downgrade():
    op.alter_column('marriage_search', 'exemplification', nullable=True, new_column_name='letter')
    op.drop_column('marriage_search', 'no_amends_copies')
    op.drop_column('marriage_search', 'no_amends')
    op.drop_column('marriage_search', 'raised_seal_copies')
    op.drop_column('marriage_search', 'raised_seal')
    op.drop_column('marriage_search', 'exemplification_copies')
    op.drop_column('marriage_search', 'alt_groom_first_name')
    op.drop_column('marriage_search', 'alt_groom_middle_name')
    op.drop_column('marriage_search', 'alt_groom_last_name')
    op.drop_column('marriage_search', 'groom_middle_name')
    op.drop_column('marriage_search', 'alt_bride_first_name')
    op.drop_column('marriage_search', 'alt_bride_middle_name')
    op.drop_column('marriage_search', 'alt_bride_last_name')
    op.drop_column('marriage_search', 'bride_middle_name')
