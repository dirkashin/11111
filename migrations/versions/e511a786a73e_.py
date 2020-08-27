"""empty message

Revision ID: e511a786a73e
Revises: 0e8ace4aad30
Create Date: 2020-08-27 15:52:45.059551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e511a786a73e'
down_revision = '0e8ace4aad30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hudong', sa.Column('hname', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hudong', 'hname')
    # ### end Alembic commands ###