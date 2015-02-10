"""empty message

Revision ID: 158f0c1b79e
Revises: 16897bc3be7
Create Date: 2015-02-08 20:43:52.505668

"""

# revision identifiers, used by Alembic.
revision = '158f0c1b79e'
down_revision = '16897bc3be7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paste',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.String(length=255), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('pastes')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pastes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('truncated_content', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='pastes_pkey')
    )
    op.drop_table('paste')
    ### end Alembic commands ###