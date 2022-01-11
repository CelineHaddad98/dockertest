"""Add new column

Revision ID: 31352704b0ce
Revises: a5f162c281f0
Create Date: 2022-01-11 08:11:51.744335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31352704b0ce'
down_revision = 'a5f162c281f0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('address', sa.Column('building_name', sa.String))


def downgrade():
    op.drop_column('address','building_name')
