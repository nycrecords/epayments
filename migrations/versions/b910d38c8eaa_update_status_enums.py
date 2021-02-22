"""Update status enums

Revision ID: b910d38c8eaa
Revises: 423df681c81f
Create Date: 2021-02-22 15:37:52.422867

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b910d38c8eaa'
down_revision = '423df681c81f'
branch_labels = None
depends_on = None

old_options = (
    'Received', 'Processing', 'Found', 'Printed', 'Mailed/Pickup', 'Emailed', 'Not_Found', 'Letter_Generated',
    'Undeliverable', 'Refunded', 'Done')
new_options = ('Received', 'Microfilm', 'Offsite', 'Processing', 'Not_Found', 'Undeliverable', 'Refund', 'Done')

old_status = sa.Enum(*old_options, name='status')
new_status = sa.Enum(*new_options, name='status')
tmp_status = sa.Enum(*new_options, name='_status')


def upgrade():
    tmp_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE _status'
               ' USING status::TEXT::_status')
    old_status.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" type type
    new_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE status'
               ' USING status::TEXT::status')
    tmp_status.drop(op.get_bind(), checkfirst=False)


def downgrade():
    # Convert 'Processing' status to 'Microfilm'
    op.execute('UPDATE suborders SET status = \'Microfilm\' WHERE status = \'Processing\'')
    op.execute(
        'UPDATE events SET new_value = jsonb_set(new_value, \'{status}\', \'"Microfilm"\'::jsonb) WHERE new_value->>\'status\' = \'Processing\'')
    op.execute(
        'UPDATE events SET previous_value = jsonb_set(previous_value, \'{status}\', \'"Microfilm"\'::jsonb) WHERE previous_value->>\'status\' = \'Processing\'')

    # Convert 'Found' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Found\'')
    op.execute(
        'UPDATE events SET new_value = jsonb_set(new_value, \'{status}\', \'"Done"\'::jsonb) WHERE new_value->>\'status\' = \'Found\'')
    op.execute(
        'UPDATE events SET previous_value = jsonb_set(previous_value, \'{status}\', \'"Done"\'::jsonb) WHERE previous_value->>\'status\' = \'Found\'')

    # Convert 'Printed' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Printed\'')
    op.execute(
        'UPDATE events SET new_value = jsonb_set(new_value, \'{status}\', \'"Done"\'::jsonb) WHERE new_value->>\'status\' = \'Printed\'')
    op.execute(
        'UPDATE events SET previous_value = jsonb_set(previous_value, \'{status}\', \'"Done"\'::jsonb) WHERE previous_value->>\'status\' = \'Printed\'')

    # Convert 'Mailed/Pickup' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Mailed/Pickup\'')
    op.execute(
        'UPDATE events SET new_value = jsonb_set(new_value, \'{status}\', \'"Done"\'::jsonb) WHERE new_value->>\'status\' = \'Mailed/Pickup\'')
    op.execute(
        'UPDATE events SET previous_value = jsonb_set(previous_value, \'{status}\', \'"Done"\'::jsonb) WHERE previous_value->>\'status\' = \'Mailed/Pickup\'')

    # Convert 'Emailed' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Emailed\'')
    op.execute(
        'UPDATE events SET new_value = jsonb_set(new_value, \'{status}\', \'"Done"\'::jsonb) WHERE new_value->>\'status\' = \'Emailed\'')
    op.execute(
        'UPDATE events SET previous_value = jsonb_set(previous_value, \'{status}\', \'"Done"\'::jsonb) WHERE previous_value->>\'status\' = \'Emailed\'')

    # Convert 'Letter_Generated' status to 'Not_Found'
    op.execute('UPDATE suborders SET status = \'Not_Found\' WHERE status = \'Letter_Generated\'')
    op.execute(
        'UPDATE events SET new_value = jsonb_set(new_value, \'{status}\', \'"Not_Found"\'::jsonb) WHERE new_value->>\'status\' = \'Letter_Generated\'')
    op.execute(
        'UPDATE events SET previous_value = jsonb_set(previous_value, \'{status}\', \'"Not_Found"\'::jsonb) WHERE previous_value->>\'status\' = \'Letter_Generated\'')

    # Create a temporary "_event_type" type, convert and drop the "new" type
    tmp_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE _status'
               ' USING status::TEXT::_status')
    new_status.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE status'
               ' USING status::TEXT::status')
    tmp_status.drop(op.get_bind(), checkfirst=False)
