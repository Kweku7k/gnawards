"""empty message

Revision ID: e2a7747dabaa
Revises: 0e955b6e00f6
Create Date: 2022-06-10 09:02:39.438727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2a7747dabaa'
down_revision = '0e955b6e00f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('award', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'award')
    # ### end Alembic commands ###
