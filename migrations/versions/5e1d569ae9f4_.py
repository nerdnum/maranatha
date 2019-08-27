"""empty message

Revision ID: 5e1d569ae9f4
Revises: d664a2cc046d
Create Date: 2019-08-20 23:17:43.243693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e1d569ae9f4'
down_revision = 'd664a2cc046d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_mobile_phone_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_mobile_phone_key', 'users', ['mobile_phone'])
    # ### end Alembic commands ###