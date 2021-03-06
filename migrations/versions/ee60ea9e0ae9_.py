"""empty message

Revision ID: ee60ea9e0ae9
Revises: 7d67b680316f
Create Date: 2017-07-06 14:12:02.770744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee60ea9e0ae9'
down_revision = '7d67b680316f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar_url')
    # ### end Alembic commands ###
