from pythonic import db,login_manager,app
from datetime import datetime
from flask_login import UserMixin
from flask_session import Session
from sqlalchemy import Sequence
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    
    try:
      candidat = Candidat.query.get(int(user_id))
      if candidat:

        return candidat
      else :
        return Recruteur.query.filter_by(id_recruteur=recruteur.id_recruteur).first()
       

      
    except:
      recruteur = Recruteur.query.get(int(user_id))
      if recruteur:
        return recruteur
        

    

   

class Candidat(db.Model,UserMixin):
    __tablename__ = 'candidat'

    id_condidat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_de_naissance = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    mot_de_passe = db.Column(db.String(60), nullable=False,unique=True)
    domaine = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    cv  = db.Column(db.String(300))
    profile_picture = db.Column(db.String(200))
    genre = db.Column(db.String(10), nullable=False, default='Unknown')
    telephone = db.Column(db.String(20),nullable=True)
    bio = db.Column(db.Text, nullable=True)
    linkedin_profile = db.Column(db.String(200), nullable=True)
    is_candidat = db.Column(db.Boolean,nullable=False,default=False)
    candidatures = db.relationship('Candidature', backref='candidat', lazy=True)

    def get_id(self):
        return str(self.id_condidat)
    def  delete(self):
        db.session.delete(self)
        db.session.commit()
        ######
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'condidat_id': self.id_condidat})
    

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(app.config['SECRET_KEY'], salt='pw-reset')
        try:
           condidat_id = s.loads(token, max_age=age)['condidat_id']
        except:
            return None
        return Candidat.query.get(condidat_id)
    
    
def update_user_password(id_candidat, new_password):
    # Retrieve the user from the database based on the user_id
    user = Candidat.query.get(id_candidat)
    
    # Update the user's password with the new_password
    user.mot_de_passe = new_password
    db.session.commit()


    # ...
    def __repr__(self):
        return f"Candidat(id_condidat={self.id_condidat}, nom={self.nom}, prenom={self.prenom}, email={self.email})"

class Recruteur(db.Model,UserMixin):
    __tablename__ = 'recruteur'

    id_recruteur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_de_societe = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(60), nullable=False, unique=True)
    domaine = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    company_description = db.Column(db.Text, nullable=True)
    is_recruteur = db.Column(db.Boolean, nullable=False, default=True)
    offres = db.relationship('OffreEmploi', backref='recruteur', lazy=True)

    def delete(self):
        # Code de suppression du compte ici
        # Par exemple, pour supprimer l'utilisateur de la base de données :
        db.session.delete(self)
        db.session.commit()
    def is_active(self):
        return True
    def get_id(self):
        return str(self.id_recruteur)
    def __str__(self):
        return self.nom_de_societe
 ########################




class OffreEmploi(db.Model):
    __tablename__ = 'offre_emploi'

    id_offre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_publication = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    date_limite = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    region = db.Column(db.String(100), nullable=False)
    competences_requises = db.Column(db.Text, nullable=True)
    diplome_requis = db.Column(db.String(100), nullable=True)
    langues_requises = db.Column(db.String(200), nullable=True)
    statut = db.Column(db.String(50), nullable=True)
    horaire_travail = db.Column(db.String(100), nullable=True)
    salaire=db.Column(db.String(100), nullable=True)
    type_de_poste=db.Column(db.String(100), nullable=True)
    categories=db.Column(db.String(100), nullable=True)
    slug = db.Column(db.String(32), nullable=False)
    recruteur_id = db.Column(db.Integer, db.ForeignKey('recruteur.id_recruteur'))
    candidatures = db.relationship('Candidature', backref='offre_emploi', lazy=True)
    #recruteur = db.relationship('Recruteur', backref='offres')

    

class Candidature(db.Model):
    __tablename__ = 'candidature'

    id_condidat = db.Column(db.Integer, db.ForeignKey('candidat.id_condidat'), nullable=False, primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('offre_emploi.id_offre'), nullable=False, primary_key=True)
    etat = db.Column(db.String(255))

    def __repr__(self):
        return f"Candidature(id={self.id}, id_candidat={self.id_candidat}, id_offre={self.id_offre})"

