"""empty message

Revision ID: 87cfa97386db
Revises: 
Create Date: 2020-10-23 06:32:24.793822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87cfa97386db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('dummy', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'dummy')
    # ### end Alembic commands ###