"""empty message

Revision ID: c55c3f4958c0
Revises: 5e1d569ae9f4
Create Date: 2019-08-21 20:49:50.231575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c55c3f4958c0'
down_revision = '5e1d569ae9f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_invitations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.Unicode(length=255), nullable=True),
    sa.Column('invited_by_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['invited_by_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_invitations')
    # ### end Alembic commands ###