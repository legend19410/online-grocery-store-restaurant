"""empty message

Revision ID: 67adc76e0b5f
Revises: 9dde494e783c
Create Date: 2021-05-14 00:28:38.148186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67adc76e0b5f'
down_revision = '9dde494e783c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('delivery_time_slot', 'status',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.create_table('max_deliveries_per_slot',
        sa.Column('max_deliveries_per_timeslot', sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint('max_deliveries_per_timeslot')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('delivery_time_slot', 'status',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
