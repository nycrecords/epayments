"""Add OCME table

Revision ID: 2c1d50b5cfa6
Revises: b910d38c8eaa
Create Date: 2022-04-05 12:55:12.981711

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2c1d50b5cfa6'
down_revision = 'b910d38c8eaa'
branch_labels = None
depends_on = None

old_options = (
    "Birth Search", "Birth Cert", "Marriage Search", "Marriage Cert", "Death Search", "Death Cert", "Tax Photo",
    "Photo Gallery", "Property Card")
new_options = old_options + ("No Amends", "OCME", "HVR")

old_type = sa.Enum(*old_options, name="order_type")
new_type = sa.Enum(*new_options, name="order_type")
tmp_type = sa.Enum(*new_options, name="_order_type")


def upgrade():
    op.create_table('ocme',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('borough', postgresql.ENUM('Bronx', 'Manhattan', 'Staten Island', 'Brooklyn', 'Queens',
                                                         name='borough', create_type=False), nullable=False),
                    sa.Column('date', sa.Date(), nullable=False),
                    sa.Column('first_name', sa.String(length=40), nullable=False),
                    sa.Column('middle_name', sa.String(length=40), nullable=True),
                    sa.Column('last_name', sa.String(length=25), nullable=False),
                    sa.Column('age', sa.String(length=3), nullable=True),
                    sa.Column('certificate_number', sa.String(length=40), nullable=True),
                    sa.Column('num_copies', sa.String(length=1), nullable=False),
                    sa.Column('raised_seal', sa.Boolean(), nullable=False),
                    sa.Column('raised_seal_copies', sa.String(length=1), nullable=True),
                    sa.Column('delivery_method',
                              postgresql.ENUM('mail', 'email', 'pickup', name='delivery_method', create_type=False),
                              nullable=False),
                    sa.Column('contact_number', sa.String(length=64), nullable=True),
                    sa.Column('contact_email', sa.String(length=256), nullable=True),
                    sa.Column('suborder_number', sa.String(length=32), nullable=False),
                    sa.ForeignKeyConstraint(['suborder_number'], ['suborders.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Update order_type enum values
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE suborders ALTER COLUMN order_type TYPE _order_type"
        " USING order_type::TEXT::_order_type"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" type type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE suborders ALTER COLUMN order_type TYPE order_type"
        " USING order_type::TEXT::order_type"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    op.drop_table('ocme')

    # Remove OCME orders from suborders
    op.execute("DELETE FROM suborders WHERE order_type = 'OCME'")
    # Create a tempoary "_type" type, convert and drop the "new" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE suborders ALTER COLUMN order_type TYPE _order_type"
        " USING order_type::TEXT::_order_type"
    )
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE suborders ALTER COLUMN order_type TYPE order_type"
        " USING order_type::TEXT::order_type"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)
