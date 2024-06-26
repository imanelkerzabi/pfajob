"""empty message

Revision ID: c1cc4c8ec516
Revises: f3034b5727a5
Create Date: 2023-06-28 07:20:52.319556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1cc4c8ec516'
down_revision = 'f3034b5727a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidat',
    sa.Column('id_condidat', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nom', sa.String(length=50), nullable=False),
    sa.Column('prenom', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('date_de_naissance', sa.DateTime(), nullable=False),
    sa.Column('mot_de_passe', sa.String(length=60), nullable=False),
    sa.Column('domaine', sa.String(length=50), nullable=False),
    sa.Column('adresse', sa.String(length=200), nullable=False),
    sa.Column('cv', sa.String(length=300), nullable=True),
    sa.Column('profile_picture', sa.String(length=200), nullable=True),
    sa.Column('genre', sa.String(length=10), nullable=False),
    sa.Column('telephone', sa.String(length=20), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('linkedin_profile', sa.String(length=200), nullable=True),
    sa.Column('is_candidat', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_condidat'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mot_de_passe')
    )
    op.create_table('recruteur',
    sa.Column('id_recruteur', sa.Integer(), nullable=False),
    sa.Column('nom_de_societe', sa.String(length=100), nullable=False),
    sa.Column('adresse', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('mot_de_passe', sa.String(length=60), nullable=False),
    sa.Column('domaine', sa.String(length=50), nullable=False),
    sa.Column('telephone', sa.String(length=20), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('company_description', sa.Text(), nullable=True),
    sa.Column('is_recruteur', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_recruteur'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mot_de_passe')
    )
    op.create_table('offre_emploi',
    sa.Column('id_offre', sa.Integer(), nullable=False),
    sa.Column('titre', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_publication', sa.DateTime(), nullable=False),
    sa.Column('date_limite', sa.DateTime(), nullable=False),
    sa.Column('region', sa.String(length=100), nullable=False),
    sa.Column('competences_requises', sa.Text(), nullable=True),
    sa.Column('diplome_requis', sa.String(length=100), nullable=True),
    sa.Column('langues_requises', sa.String(length=200), nullable=True),
    sa.Column('statut', sa.String(length=50), nullable=True),
    sa.Column('horaire_travail', sa.String(length=100), nullable=True),
    sa.Column('salaire', sa.String(length=100), nullable=True),
    sa.Column('type_de_poste', sa.String(length=100), nullable=True),
    sa.Column('categories', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=32), nullable=False),
    sa.Column('id_recruteur', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_recruteur'], ['recruteur.id_recruteur'], ),
    sa.PrimaryKeyConstraint('id_offre')
    )
    op.create_table('candidature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_condidat', sa.Integer(), nullable=False),
    sa.Column('id_offre', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_condidat'], ['candidat.id_condidat'], ),
    sa.ForeignKeyConstraint(['id_offre'], ['offre_emploi.id_offre'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidature')
    op.drop_table('offre_emploi')
    op.drop_table('recruteur')
    op.drop_table('candidat')
    # ### end Alembic commands ###
