"""empty message

Revision ID: 791e55908e7c
Revises: 
Create Date: 2025-02-28 20:46:13.461899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '791e55908e7c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('height', sa.String(), nullable=True),
    sa.Column('mass', sa.String(), nullable=True),
    sa.Column('hair_color', sa.String(), nullable=True),
    sa.Column('skin_color', sa.String(), nullable=True),
    sa.Column('eye_color', sa.String(), nullable=True),
    sa.Column('birth_year', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('diameter', sa.String(), nullable=True),
    sa.Column('rotation_period', sa.String(), nullable=True),
    sa.Column('orbital_period', sa.String(), nullable=True),
    sa.Column('gravity', sa.String(), nullable=True),
    sa.Column('population', sa.String(), nullable=True),
    sa.Column('climate', sa.String(), nullable=True),
    sa.Column('terrain', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('character_favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('following_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet_favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Title'),
    sa.UniqueConstraint('image_url')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_type', sa.Enum('reel', 'image', 'video', name='type'), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medias')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('planet_favorites')
    op.drop_table('followers')
    op.drop_table('character_favorites')
    op.drop_table('users')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
