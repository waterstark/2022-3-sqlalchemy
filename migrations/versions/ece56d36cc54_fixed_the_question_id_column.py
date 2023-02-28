"""Fixed the question_id column

Revision ID: ece56d36cc54
Revises: 77df5700c81a
Create Date: 2023-02-28 17:01:02.290417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece56d36cc54'
down_revision = '77df5700c81a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('question_id', sa.Integer(), nullable=False))
    op.drop_constraint('answers_questions_id_fkey', 'answers', type_='foreignkey')
    op.create_foreign_key(None, 'answers', 'questions', ['question_id'], ['id'], ondelete='CASCADE')
    op.drop_column('answers', 'questions_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('questions_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'answers', type_='foreignkey')
    op.create_foreign_key('answers_questions_id_fkey', 'answers', 'questions', ['questions_id'], ['id'], ondelete='CASCADE')
    op.drop_column('answers', 'question_id')
    # ### end Alembic commands ###