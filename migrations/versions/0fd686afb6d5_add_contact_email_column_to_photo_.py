"""Add contact_email column to photo_gallery table

Revision ID: 0fd686afb6d5
Revises: 0f114a99e5cf
Create Date: 2022-04-06 15:13:04.315459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0fd686afb6d5'
down_revision = '0f114a99e5cf'
branch_labels = None
depends_on = None

old_options = ("1940", "1980", "Both")
new_options = old_options + ("Luna",)

old_type = sa.Enum(*old_options, name="collection")
new_type = sa.Enum(*new_options, name="collection")
tmp_type = sa.Enum(*new_options, name="_collection")


def upgrade():
    # Add contact_email column
    op.add_column('photo_gallery', sa.Column('contact_email', sa.String(length=256), nullable=True))
    op.add_column('tax_photo', sa.Column('contact_email', sa.String(length=256), nullable=True))

    # Update size column to be nullable
    op.alter_column('photo_gallery', 'size', nullable=True)
    op.alter_column('tax_photo', 'size', nullable=True)

    # Update collection enum values
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE tax_photo ALTER COLUMN collection TYPE _collection"
        " USING collection::TEXT::_collection"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" type type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE tax_photo ALTER COLUMN collection TYPE collection"
        " USING collection::TEXT::collection"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    op.drop_column('photo_gallery', 'contact_email')
    op.drop_column('tax_photo', 'contact_email')

    # Create a tempoary "_type" type, convert and drop the "new" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE tax_photo ALTER COLUMN collection TYPE _collection"
        " USING collection::TEXT::_collection"
    )
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" type type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE tax_photo ALTER COLUMN collection TYPE collection"
        " USING collection::TEXT::collection"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)
