"""empty message

Revision ID: 880a04bd6f74
Revises: 8072d16722ce
Create Date: 2020-08-04 18:30:51.317703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '880a04bd6f74'
down_revision = '8072d16722ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website_link')
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###
