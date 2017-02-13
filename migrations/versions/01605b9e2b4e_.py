"""empty message

Revision ID: 01605b9e2b4e
Revises: 1d27abb9fe5a
Create Date: 2017-01-13 15:16:52.837123

"""

# revision identifiers, used by Alembic.
revision = '01605b9e2b4e'
down_revision = '1d27abb9fe5a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('orderno', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('clientagencyname', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptoname', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptostreetadd', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptostreetadd2', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptocity', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptostate', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptozipcode', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('shiptocountry', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shiptophone', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('customeremail', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('shippinginstructions', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('clientsdata', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('confirmationmessage', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('datereceived', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('billingname', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('datelastmodified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('suborderno', sa.INTEGER(), nullable=False),
    sa.Column('clientid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ordertypes', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('suborderno', name='order_pkey')
    )
    ### end Alembic commands ###