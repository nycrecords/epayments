"""Initial migration

Revision ID: bcf911ebbb8c
Revises:
Create Date: 2017-11-28 01:39:24.264735

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bcf911ebbb8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('date_submitted', sa.DateTime(), nullable=False),
    sa.Column('date_received', sa.DateTime(), nullable=True),
    sa.Column('confirmation_message', sa.Text(), nullable=False),
    sa.Column('client_data', sa.Text(), nullable=False),
    sa.Column('order_types', postgresql.ARRAY(sa.Text()), nullable=True),
    sa.Column('multiple_items', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('email'),
    sa.UniqueConstraint('email')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('billing_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('shipping_name', sa.String(length=64), nullable=False),
    sa.Column('address_line_1', sa.String(length=64), nullable=True),
    sa.Column('address_line_2', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=False),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('zip_code', sa.String(length=64), nullable=False),
    sa.Column('country', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('instructions', sa.String(length=64), nullable=True),
    sa.Column('order_number', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['order_number'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suborder',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('client_agency_name', sa.String(length=64), nullable=False),
    sa.Column('order_number', sa.String(length=64), nullable=False),
    sa.Column('status', sa.Enum('Received', 'Processing', 'Found', 'Printed', 'Mailed/Pickup', 'Not_Found', 'Letter_Generated', 'Undeliverable', 'Done', name='status'), nullable=True),
    sa.ForeignKeyConstraint(['order_number'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('birth_cert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('certificate_no', sa.String(length=40), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('mid_name', sa.String(length=40), nullable=True),
    sa.Column('gender_type', sa.Enum('Not_Known', 'Male', 'Female', name='gender_type'), nullable=True),
    sa.Column('father_name', sa.String(length=40), nullable=True),
    sa.Column('mother_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('num_copies', sa.String(length=4), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('birth_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
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
    sa.Column('num_copies', sa.String(length=4), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('birth_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
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
    sa.Column('num_copies', sa.String(length=40), nullable=True),
    sa.Column('cemetery', sa.String(length=40), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('death_place', sa.String(length=40), nullable=True),
    sa.Column('age_of_death', sa.String(length=3), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('death_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('mid_name', sa.String(length=40), nullable=True),
    sa.Column('relationship', sa.String(length=30), nullable=True),
    sa.Column('purpose', sa.Enum('Genealogical/Historical', 'Personal Use', 'Legal', 'Immigration', 'Medicaid/Social Security', 'Health', 'Other', name='purpose'), nullable=False),
    sa.Column('num_copies', sa.String(length=40), nullable=True),
    sa.Column('cemetery', sa.String(length=40), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('death_place', sa.String(length=40), nullable=True),
    sa.Column('age_of_death', sa.String(length=3), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('suborder_number', sa.String(length=32), nullable=True),
    sa.Column('user_email', sa.String(length=100), nullable=True),
    sa.Column('type', sa.Enum('update_status', 'update_photo_tax', 'initial_import', name='event_type'), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('previous_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('new_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
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
    sa.Column('num_copies', sa.String(length=40), nullable=False),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=True),
    sa.Column('marriage_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
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
    sa.Column('num_copies', sa.String(length=40), nullable=False),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.String(length=2), nullable=True),
    sa.Column('years', postgresql.ARRAY(sa.String(length=4), dimensions=1), nullable=False),
    sa.Column('marriage_place', sa.String(length=40), nullable=True),
    sa.Column('borough', postgresql.ARRAY(sa.String(length=20), dimensions=1), nullable=False),
    sa.Column('letter', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo_gallery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('additional_description', sa.String(length=50), nullable=True),
    sa.Column('size', sa.Enum('8x10', '11x14', '16x20', name='size'), nullable=False),
    sa.Column('num_copies', sa.String(length=2), nullable=False),
    sa.Column('mail_pickup', sa.Boolean(), nullable=False),
    sa.Column('contact_number', sa.String(length=10), nullable=True),
    sa.Column('personal_use_agreement', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo_tax',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collection', sa.Enum('1940', '1980', 'Both', name='collection'), nullable=False),
    sa.Column('borough', sa.Enum('Bronx', 'Manhattan', 'Staten Island', 'Brooklyn', 'Queens', name='borough'), nullable=False),
    sa.Column('roll', sa.String(length=9), nullable=True),
    sa.Column('block', sa.String(length=9), nullable=True),
    sa.Column('lot', sa.String(length=9), nullable=True),
    sa.Column('street_number', sa.String(length=10), nullable=False),
    sa.Column('street', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=35), nullable=True),
    sa.Column('type', sa.Enum('8x10', '11x14', name='type'), nullable=False),
    sa.Column('size', sa.Enum('8x10', '11x14', '16x20', name='size'), nullable=True),
    sa.Column('num_copies', sa.String(length=2), nullable=False),
    sa.Column('mail_pickup', sa.Boolean(), nullable=True),
    sa.Column('contact_number', sa.String(length=10), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prop_card',
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
    sa.Column('suborder_number', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['suborder_number'], ['suborder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prop_card')
    op.drop_table('photo_tax')
    op.drop_table('photo_gallery')
    op.drop_table('marriage_search')
    op.drop_table('marriage_cert')
    op.drop_table('event')
    op.drop_table('death_search')
    op.drop_table('death_cert')
    op.drop_table('birth_search')
    op.drop_table('birth_cert')
    op.drop_table('suborder')
    op.drop_table('customer')
    op.drop_table('users')
    op.drop_table('order')
    # ### end Alembic commands ###
