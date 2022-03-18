"""empty message

Revision ID: 1226585ae581
Revises: a60bea19caaf
Create Date: 2022-03-18 00:51:38.879859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1226585ae581'
down_revision = 'a60bea19caaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sub_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('mainCategory', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('candidates', sa.Column('category', sa.String(), nullable=True))
    op.add_column('candidates', sa.Column('subcategory', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('candidates', 'subcategory')
    op.drop_column('candidates', 'category')
    op.drop_table('sub_category')
    # ### end Alembic commands ###
