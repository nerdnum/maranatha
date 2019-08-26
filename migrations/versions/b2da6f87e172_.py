"""empty message

Revision ID: b2da6f87e172
Revises: 
Create Date: 2019-08-19 21:29:38.044188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2da6f87e172'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Unicode(length=255), nullable=True),
    sa.Column('mobile_phone', sa.String(length=15), nullable=True),
    sa.Column('first_name', sa.Unicode(length=50), nullable=False),
    sa.Column('last_name', sa.Unicode(length=50), nullable=False),
    sa.Column('user_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
