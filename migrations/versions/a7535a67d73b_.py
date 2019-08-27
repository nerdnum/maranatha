"""empty message

Revision ID: a7535a67d73b
Revises: 929224607db7
Create Date: 2019-08-25 23:30:04.938376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7535a67d73b'
down_revision = '929224607db7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login', sa.DATE(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###