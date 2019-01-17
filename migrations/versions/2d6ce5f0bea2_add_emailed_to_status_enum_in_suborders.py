"""Add 'Emailed' to status enum in suborders

Revision ID: 2d6ce5f0bea2
Revises: 3805d51e5bdd
Create Date: 2019-01-17 21:50:10.559077

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2d6ce5f0bea2'
down_revision = '3805d51e5bdd'
branch_labels = None
depends_on = None

old_options = (
    'Received', 'Processing', 'Found', 'Printed', 'Mailed/Pickup', 'Not_Found', 'Letter_Generated', 'Undeliverable',
    'Refunded', 'Done')
new_options = old_options + ('Emailed',)

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
    # Convert 'Emailed' status to 'Mailed/Pickup'
    op.execute('UPDATE suborders SET status = \'Mailed/Pickup\' WHERE status = \'Emailed\'')
    # Create a tempoary "_event_type" type, convert and drop the "new" type
    tmp_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE _status'
               ' USING status::TEXT::_status')
    new_status.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_status.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE suborders ALTER COLUMN status TYPE status'
               ' USING status::TEXT::status')
    tmp_status.drop(op.get_bind(), checkfirst=False)
