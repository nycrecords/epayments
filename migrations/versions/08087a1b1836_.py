"""empty message

Revision ID: 08087a1b1836
Revises: None
Create Date: 2017-06-06 14:38:01.469985

"""

# revision identifiers, used by Alembic.
revision = '08087a1b1836'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('address_line_1', sa.String(length=64), nullable=True),
    sa.Column('address_line_2', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=False),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('zip_code', sa.String(length=64), nullable=False),
    sa.Column('country', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('instructions', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('order_no', sa.String(length=64), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.Column('date_submitted', sa.DateTime(), nullable=False),
    sa.Column('date_received', sa.DateTime(), nullable=True),
    sa.Column('billing_name', sa.String(length=64), nullable=False),
    sa.Column('customer_email', sa.String(length=64), nullable=False),
    sa.Column('confirmation_message', sa.Text(), nullable=False),
    sa.Column('client_data', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('sub_order_no')
    )
    op.create_table('birth_cert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('mid_name', sa.String(length=40), nullable=True),
    sa.Column('gender_type', sa.Enum('Not_Known', 'Male', 'Female', name='gender_type'), nullable=True),
    sa.Column('father_name', sa.String(length=40), nullable=True),
    sa.Column('mother_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('additional_copy', sa.String(length=4), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('birth_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('birth_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('mid_name', sa.String(length=40), nullable=True),
    sa.Column('gender_type', sa.Enum('Not_Known', 'Male', 'Female', name='gender_type'), nullable=True),
    sa.Column('father_name', sa.String(length=40), nullable=True),
    sa.Column('mother_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('additional_copy', sa.String(length=4), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('birth_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('death_cert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('certificate_no', sa.String(length=40), nullable=False),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('mid_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('copy_req', sa.String(length=40), nullable=True),
    sa.Column('cemetery', sa.String(length=40), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('death_place', sa.String(length=40), nullable=True),
    sa.Column('age_of_death', sa.String(length=3), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('death_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('mid_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('copy_req', sa.String(length=40), nullable=True),
    sa.Column('cemetery', sa.String(length=40), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('death_place', sa.String(length=40), nullable=True),
    sa.Column('age_of_death', sa.String(length=3), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('marriage_cert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('certificate_no', sa.String(length=40), nullable=True),
    sa.Column('groom_last_name', sa.String(length=25), nullable=False),
    sa.Column('groom_first_name', sa.String(length=40), nullable=True),
    sa.Column('bride_last_name', sa.String(length=25), nullable=False),
    sa.Column('bride_first_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('copy_req', sa.String(length=40), nullable=False),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('marriage_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('marriage_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('groom_last_name', sa.String(length=25), nullable=False),
    sa.Column('groom_first_name', sa.String(length=40), nullable=True),
    sa.Column('bride_last_name', sa.String(length=25), nullable=False),
    sa.Column('bride_first_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('copy_req', sa.String(length=40), nullable=False),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=False),
    sa.Column('marriage_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo_gallery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('additional_description', sa.String(length=50), nullable=True),
    sa.Column('size', sa.Enum('8x10', '11x14', '16x20', name='size'), nullable=False),
    sa.Column('copy', sa.String(length=2), nullable=False),
    sa.Column('mail_pickup', sa.Boolean(), nullable=False),
    sa.Column('contact_no', sa.String(length=10), nullable=True),
    sa.Column('personal_use_agreement', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo_tax',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collection', sa.Enum('1940', '1980', 'Both', name='collection'), nullable=False),
    sa.Column('borough', sa.Enum('Bronx', 'Manhattan', 'Satan Island', 'Brooklyn', 'Queens', name='borough'), nullable=False),
    sa.Column('roll', sa.String(length=9), nullable=True),
    sa.Column('block', sa.String(length=9), nullable=True),
    sa.Column('lot', sa.String(length=9), nullable=True),
    sa.Column('street_no', sa.String(length=10), nullable=False),
    sa.Column('street', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=35), nullable=True),
    sa.Column('type', sa.Enum('8x10', '11x14', name='type'), nullable=False),
    sa.Column('size', sa.Enum('8x10', '11x14', '16x20', name='size'), nullable=True),
    sa.Column('copies', sa.String(length=2), nullable=False),
    sa.Column('mail_pickup', sa.Boolean(), nullable=True),
    sa.Column('contact_no', sa.String(length=10), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('propCard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('block', sa.String(length=9), nullable=True),
    sa.Column('lot', sa.String(length=9), nullable=True),
    sa.Column('building_no', sa.String(length=10), nullable=False),
    sa.Column('street', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=40), nullable=True),
    sa.Column('certified', sa.Boolean(), nullable=False),
    sa.Column('mail_pickup', sa.Boolean(), nullable=False),
    sa.Column('contact_info', sa.String(length=35), nullable=True),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sub_order_no', sa.BigInteger(), nullable=True),
    sa.Column('current_status', sa.Enum('Received', 'Processing', 'Found', 'Mailed/Pickup', 'Not_Found', 'Letter_Generated', 'Undeliverable', 'Done', name='current_status'), nullable=False),
    sa.ForeignKeyConstraint(['sub_order_no'], ['orders.sub_order_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status')
    op.drop_table('propCard')
    op.drop_table('photo_tax')
    op.drop_table('photo_gallery')
    op.drop_table('marriage_search')
    op.drop_table('marriage_cert')
    op.drop_table('death_search')
    op.drop_table('death_cert')
    op.drop_table('birth_search')
    op.drop_table('birth_cert')
    op.drop_table('orders')
    op.drop_table('customer')
    ### end Alembic commands ###
