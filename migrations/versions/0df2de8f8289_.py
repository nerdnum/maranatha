"""empty message

Revision ID: 0df2de8f8289
Revises: 0593e93dc3f8
Create Date: 2020-06-11 19:33:11.830353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0df2de8f8289'
down_revision = '0593e93dc3f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_invitations', sa.Column('password', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_invitations', 'password')
    # ### end Alembic commands ###
