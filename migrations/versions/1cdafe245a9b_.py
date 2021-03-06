"""empty message

Revision ID: 1cdafe245a9b
Revises: a4e00f1d51cb
Create Date: 2020-08-25 21:27:17.509557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cdafe245a9b'
down_revision = 'a4e00f1d51cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('nickname', table_name='essay')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('nickname', 'essay', ['nickname'], unique=True)
    # ### end Alembic commands ###
