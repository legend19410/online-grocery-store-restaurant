"""empty message

Revision ID: 1097845ee79d
Revises: 59dccd722ede
Create Date: 2021-03-02 11:06:14.808739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1097845ee79d'
down_revision = '59dccd722ede'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food', sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('food', 'price')
    # ### end Alembic commands ###
