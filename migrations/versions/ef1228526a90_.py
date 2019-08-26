"""empty message

Revision ID: ef1228526a90
Revises: a5ac39265743
Create Date: 2019-08-25 12:50:24.110855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef1228526a90'
down_revision = 'a5ac39265743'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('country_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('populated_area_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('subdivision_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'populated_areas', ['populated_area_id'], ['id'])
    op.create_foreign_key(None, 'users', 'countries', ['country_id'], ['id'])
    op.create_foreign_key(None, 'users', 'subdivisions', ['subdivision_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'subdivision_id')
    op.drop_column('users', 'populated_area_id')
    op.drop_column('users', 'country_id')
    # ### end Alembic commands ###
