"""empty message

Revision ID: 086c6c032c40
Revises: 4fcf3afde901
Create Date: 2020-06-11 20:11:07.006848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '086c6c032c40'
down_revision = '4fcf3afde901'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_invitations', sa.Column('invitation_sent', sa.DateTime(), nullable=True))
    op.add_column('user_invitations', sa.Column('user_responded', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_invitations', 'user_responded')
    op.drop_column('user_invitations', 'invitation_sent')
    # ### end Alembic commands ###
