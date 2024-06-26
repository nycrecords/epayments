"""Remove mail from Tax Photo and PhotoGallery

Revision ID: 175096050ecc
Revises: 32c352490472
Create Date: 2018-10-02 15:20:05.164018

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '175096050ecc'
down_revision = '32c352490472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo_gallery', 'mail')
    op.drop_column('tax_photo', 'mail')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tax_photo', sa.Column('mail', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('photo_gallery', sa.Column('mail', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
