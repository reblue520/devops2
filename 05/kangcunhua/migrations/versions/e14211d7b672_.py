"""empty message

Revision ID: e14211d7b672
Revises: 1d24c8791efa
Create Date: 2016-06-18 13:47:51.493410

"""

# revision identifiers, used by Alembic.
revision = 'e14211d7b672'
down_revision = '1d24c8791efa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('server', sa.Column('idc_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('server', 'idc_id')
    ### end Alembic commands ###
