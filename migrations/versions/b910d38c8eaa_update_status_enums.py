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
new_options = ('Microfilm', 'Offsite', 'Processing', 'Refund')
all_options = set(list(old_options) + list(new_options))
final_options = ('Received', 'Microfilm', 'Offsite', 'Processing', 'Not_Found', 'Undeliverable', 'Refund', 'Done')

old_status = sa.Enum(*old_options, name='status')
new_status = sa.Enum(*final_options, name='status')
tmp_status = sa.Enum(*all_options, name='_status')


def upgrade():
    tmp_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE _status'
               ' USING status::TEXT::_status')
    old_status.drop(op.get_bind(), checkfirst=False)

    # Convert 'Processing' status to 'Microfilm'
    op.execute('UPDATE suborders SET status = \'Microfilm\' WHERE status = \'Processing\'')

    # Convert 'Found' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Found\'')

    # Convert 'Printed' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Printed\'')

    # Convert 'Mailed/Pickup' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Mailed/Pickup\'')

    # Convert 'Emailed' status to 'Done'
    op.execute('UPDATE suborders SET status = \'Done\' WHERE status = \'Emailed\'')

    # Convert 'Letter_Generated' status to 'Not_Found'
    op.execute('UPDATE suborders SET status = \'Not_Found\' WHERE status = \'Letter_Generated\'')

    # Create and convert to the "new" type type
    new_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE status'
               ' USING status::TEXT::status')
    tmp_status.drop(op.get_bind(), checkfirst=False)


def downgrade():
    # It is not possible to downgrade and migrate the status data.
    pass
