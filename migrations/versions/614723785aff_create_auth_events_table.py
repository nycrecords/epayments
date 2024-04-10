
"""create auth events table

Revision ID: 614723785aff
Revises: bfb60868b768
Create Date: 2023-09-11 14:23:18.052839

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import false
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '614723785aff'
down_revision = 'bfb60868b768'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('guid', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('first_name', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('middle_initial', sa.String(length=1), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('email_validated', sa.Boolean(), nullable=False, server_default=false()))
        batch_op.add_column(
            sa.Column('last_sign_in_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('session_id', sa.String(length=254), nullable=True))
        batch_op.drop_constraint('users_email_key', type_='unique')
        batch_op.create_unique_constraint(None, ['guid'])
        batch_op.drop_column('password_hash')

    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )

    op.create_table('user_roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.String(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.guid'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('auth_events',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_guid', sa.String(), nullable=False),
                    sa.Column('type', sa.Enum('user_created', 'user_logged_in', 'user_failed_login',
                                              'user_logged_out', 'user_role_changed', 'agency_user_activated',
                                              'agency_user_deactivated', name='auth_event_type'), nullable=False),
                    sa.Column('previous_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('new_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_guid'], ['users.guid'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table('user_roles')
    op.drop_table('roles')
    op.drop_table('auth_events')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
        batch_op.create_unique_constraint('users_email_key', ['email'])
        batch_op.drop_column('session_id')
        batch_op.drop_column('last_sign_in_at')
        batch_op.drop_column('email_validated')
        batch_op.drop_column('last_name')
        batch_op.drop_column('middle_initial')
        batch_op.drop_column('first_name')
        batch_op.drop_column('guid')

    # ### end Alembic commands ###
