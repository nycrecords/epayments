"""update_orders_and_events_table

Revision ID: bfb60868b768
Revises: 09a40dc15d98
Create Date: 2023-08-10 13:38:30.275665

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bfb60868b768'
down_revision = '09a40dc15d98'
branch_labels = None
depends_on = None

# Enum 'type' for PostgreSQL
enum_name = 'event_type'
# Set temporary enum 'type' for PostgreSQL
tmp_enum_name = 'tmp_' + enum_name

old_options = ('initial_import', 'update_status', 'update_tax_photo', 'order_created',)
new_options = old_options + ('update_check_mo_number',)

# Create enum fields
old_type = sa.Enum(*old_options, name=enum_name)
new_type = sa.Enum(*new_options, name=enum_name)

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_number', sa.String(length=64), nullable=True))
        batch_op.create_foreign_key(None, 'orders', ['order_number'], ['id'])

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('check_mo_number', sa.String(length=128), nullable=True))

    # Rename current enum type to tmp_
    op.execute('ALTER TYPE ' + enum_name + ' RENAME TO ' + tmp_enum_name)
    # Create new enum type in db
    new_type.create(op.get_bind())
    # Update column to use new enum type
    op.execute('ALTER TABLE events ALTER COLUMN type TYPE ' + enum_name + ' USING type::text::' + enum_name)
    # Drop old enum type
    op.execute('DROP TYPE ' + tmp_enum_name)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('check_mo_number')

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('order_number')

    # Instantiate db query
    audit = sa.sql.table('events', sa.Column('type', new_type, nullable=False))
    # Convert update_check_mo_number to initial_import
    op.execute(audit.update().where(audit.c.type == u'update_check_mo_number').values(type='initial_import'))
    # Rename enum type to tmp_
    op.execute('ALTER TYPE ' + enum_name + ' RENAME TO ' + tmp_enum_name)
    # Create enum type using old values
    old_type.create(op.get_bind())
    # Set enum type as type for event_type column
    op.execute(
        'ALTER TABLE events ALTER COLUMN type TYPE ' + enum_name + ' USING type::text::' + enum_name)
    # Drop temp enum type
    op.execute('DROP TYPE ' + tmp_enum_name)

    # ### end Alembic commands ###
