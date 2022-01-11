"""add uuid

Revision ID: 89592f6702dd
Revises: 
Create Date: 2022-01-10 16:38:30.873899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89592f6702dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
