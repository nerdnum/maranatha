"""empty message

Revision ID: f986cd693f6e
Revises: 889a1777d874
Create Date: 2020-07-06 14:43:56.151186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f986cd693f6e'
down_revision = '889a1777d874'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_invitations_email_key', 'user_invitations', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_invitations_email_key', 'user_invitations', ['email'])
    # ### end Alembic commands ###
