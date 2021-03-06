"""empty message

Revision ID: 4fcf3afde901
Revises: 0df2de8f8289
Create Date: 2020-06-11 19:36:37.262487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fcf3afde901'
down_revision = '0df2de8f8289'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_invitations', sa.Column('is_bulk_invite', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_invitations', 'is_bulk_invite')
    # ### end Alembic commands ###
