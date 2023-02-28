"""Fixed the question_id column

Revision ID: 54b424e67e76
Revises: ece56d36cc54
Create Date: 2023-02-28 17:08:30.898216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54b424e67e76'
down_revision = 'ece56d36cc54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('questions_id', sa.Integer(), nullable=False))
    op.drop_constraint('answers_question_id_fkey', 'answers', type_='foreignkey')
    op.create_foreign_key(None, 'answers', 'questions', ['questions_id'], ['id'], ondelete='CASCADE')
    op.drop_column('answers', 'question_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'answers', type_='foreignkey')
    op.create_foreign_key('answers_question_id_fkey', 'answers', 'questions', ['question_id'], ['id'], ondelete='CASCADE')
    op.drop_column('answers', 'questions_id')
    # ### end Alembic commands ###