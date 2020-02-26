"""empty message

Revision ID: d485d85d51f2
Revises: 
Create Date: 2020-02-25 21:56:20.762108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd485d85d51f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model1',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('surname', sa.String(length=80), nullable=True),
    sa.Column('fathername', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('sex', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('grate', sa.String(), nullable=True),
    sa.Column('education', sa.String(), nullable=True),
    sa.Column('foreign_languges', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('start_place', sa.String(), nullable=True),
    sa.Column('nationality', sa.String(), nullable=True),
    sa.Column('marriage', sa.String(length=10), nullable=True),
    sa.Column('about_myself', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('organisation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('creation_date', sa.Date(), nullable=True),
    sa.Column('personnel_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personnel_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organisation')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('news_table')
    op.drop_table('model1')
    # ### end Alembic commands ###