"""Update nullable columns

Revision ID: 32c352490472
Revises: 3bb2c6ca0e3e
Create Date: 2018-10-02 00:34:43.822096

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '32c352490472'
down_revision = '3bb2c6ca0e3e'
branch_labels = None
depends_on = None

old_options = ('initial_import', 'update_status', 'update_tax_photo')
new_options = old_options + ('order_created',)

old_type = sa.Enum(*old_options, name='event_type')
new_type = sa.Enum(*new_options, name='event_type')
tmp_type = sa.Enum(*new_options, name='_event_type')


def upgrade():
    # Create a temporary "_event_type" type, convert and drop the "old" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE events ALTER COLUMN type TYPE _event_type'
               ' USING type::TEXT::_event_type')
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" type type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE events ALTER COLUMN type TYPE event_type'
               ' USING type::TEXT::event_type')
    tmp_type.drop(op.get_bind(), checkfirst=False)

    # Update nullable columns
    op.alter_column('orders', 'client_data',
                    existing_type=sa.TEXT(),
                    nullable=True)
    op.alter_column('orders', 'confirmation_message',
                    existing_type=sa.TEXT(),
                    nullable=True)
    op.alter_column('suborders', 'client_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)

    # Set email to be unique in users table
    op.create_unique_constraint(None, 'users', ['email'])


def downgrade():
    # Convert 'order_created' type into 'initial_import'
    op.execute('UPDATE events SET type = \'initial_import\' WHERE type = \'order_created\'')
    # Create a tempoary "_event_type" type, convert and drop the "new" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE events ALTER COLUMN type TYPE _event_type'
               ' USING type::TEXT::_event_type')
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE events ALTER COLUMN type TYPE event_type'
               ' USING type::TEXT::event_type')
    tmp_type.drop(op.get_bind(), checkfirst=False)

    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('suborders', 'client_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.alter_column('orders', 'confirmation_message',
                    existing_type=sa.TEXT(),
                    nullable=False)
    op.alter_column('orders', 'client_data',
                    existing_type=sa.TEXT(),
                    nullable=False)
