"""empty message

Revision ID: cc0eaf2afed5
Revises: c1cc4c8ec516
Create Date: 2023-06-28 07:28:00.630439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc0eaf2afed5'
down_revision = 'c1cc4c8ec516'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('offre_emploi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('idrec', sa.Integer(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'recruteur', ['idrec'], ['id_recruteur'])
        batch_op.drop_column('id_recruteur')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('offre_emploi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_recruteur', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'recruteur', ['id_recruteur'], ['id_recruteur'])
        batch_op.drop_column('idrec')

    # ### end Alembic commands ###