"""v3

Revision ID: 20df8db7546f
Revises: 3e4c19ba3380
Create Date: 2024-12-28 17:03:38.785621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20df8db7546f'
down_revision: Union[str, None] = '3e4c19ba3380'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('GameMessage',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('result_id', sa.String(length=128), nullable=False),
    sa.Column('inline_message_id', sa.String(length=128), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_GameMessage')),
    sa.UniqueConstraint('id', name=op.f('uq_GameMessage_id'))
    )
    op.create_table('Theme',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('id_str', sa.String(length=128), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Theme')),
    sa.UniqueConstraint('id', name=op.f('uq_Theme_id'))
    )
    op.create_table('Word',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('trans', sa.JSON(), nullable=False),
    sa.Column('themeId', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['themeId'], ['Theme.id'], name=op.f('fk_Word_themeId_Theme')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_Word')),
    sa.UniqueConstraint('id', name=op.f('uq_Word_id'))
    )
    op.create_table('UserWord',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('wordId', sa.Integer(), nullable=False),
    sa.Column('tryies', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], name=op.f('fk_UserWord_userId_User')),
    sa.ForeignKeyConstraint(['wordId'], ['Word.id'], name=op.f('fk_UserWord_wordId_Word')),
    sa.PrimaryKeyConstraint('userId', 'wordId', name=op.f('pk_UserWord'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserWord')
    op.drop_table('Word')
    op.drop_table('Theme')
    op.drop_table('GameMessage')
    # ### end Alembic commands ###
