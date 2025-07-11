"""Add status to Project model

Revision ID: f359421b1a31
Revises: 3e2b165ae55e
Create Date: 2025-06-14 15:17:49.483910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f359421b1a31'
down_revision = '3e2b165ae55e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
