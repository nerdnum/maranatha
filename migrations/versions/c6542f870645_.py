"""empty message

Revision ID: c6542f870645
Revises: a7535a67d73b
Create Date: 2019-08-25 23:30:24.781037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6542f870645'
down_revision = 'a7535a67d73b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_login')
    # ### end Alembic commands ###
