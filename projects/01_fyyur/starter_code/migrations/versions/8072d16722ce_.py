"""empty message

Revision ID: 8072d16722ce
Revises: 1dbdb04a57f3
Create Date: 2020-08-03 01:23:31.320180

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8072d16722ce'
down_revision = '1dbdb04a57f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.execute('UPDATE "Show" set start_time = date_time WHERE start_time IS NULL;')
    op.alter_column('Show', 'start_time', nullable=False)
    op.drop_column('Show', 'date_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###
