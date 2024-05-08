from flask_wtf import FlaskForm
from pythonic.models import Candidat, Recruteur
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, SubmitField,BooleanField, DateField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,Length,URL
from flask_login import current_user
from flask_ckeditor import CKEditorField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
)
from pythonic.models import Candidat,Recruteur


class RegistrationCandidat(FlaskForm):
    genre_choices = [('M', 'Masculin'), ('F', 'Féminin')]
    nom = StringField('Nom', validators=[DataRequired(),Length(min=3, max=20)])
    prenom = StringField('Prénom', validators=[DataRequired(),Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(),])
    password = PasswordField('Mot de passe', validators=[DataRequired(),Length(min=8, max=20)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password'),Length(min=8, max=20)])
    genre = SelectField('Genre', choices=genre_choices, validators=[DataRequired()])
    date_naissance = StringField('Date de naissance', validators=[DataRequired()])  # Ajout du champ date de naissance
    domaine = StringField('Domaine', validators=[DataRequired()])  # Ajout du champ domaine
    telephone = StringField('telephone', validators=[DataRequired()])  # Ajout du champ adresse

    adresse = StringField('Ville', validators=[DataRequired()])  # Ajout du champ adresse
    #cv = FileField('CV', validators=[DataRequired()])
    cv = FileField('CV', validators=[DataRequired(), FileAllowed(['pdf'], 'Only PDF files allowed.')])

    profile_picture = FileField('photo de profil', validators=[DataRequired(),FileAllowed(['png', 'jpg', 'jpeg'], 'Only PNG and JPEG files allowed.')])
    submit = SubmitField("S'inscrire")
     
    def validate_email(self, email):
        candidat = Candidat.query.filter_by(email=email.data).first()
        if candidat:
            raise ValidationError("L'adresse e-mail existe déjà ! Veuillez en choisir une autre.")

class RegistrationRecruteur(FlaskForm):
    nom_societe = StringField('Nom de la société', validators=[DataRequired(),Length(min=3, max=20)])
    adresse = StringField('Adresse', validators=[DataRequired(),Length(min=3, max=300)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(),Length(min=8, max=20)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password'),Length(min=8, max=20)])
    domaine = StringField('Domaine', validators=[DataRequired()])  # Ajout du champ domaine
    telephone =StringField('Telephone', validators=[DataRequired()])  
    submit = SubmitField("S'inscrire")
    def validate_email(self, email):
        recruteur = Recruteur.query.filter_by(email=email.data).first()
        if recruteur:
            raise ValidationError("L'adresse e-mail existe déjà ! Veuillez en choisir une autre.")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')
#--------------
class ChangePasswordcondForm(FlaskForm):
    password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Changer le mot de passe')

##-------------
class ChangePasswordrecdForm(FlaskForm):
    password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Changer le mot de passe')


class UpdateProfileFormcondidat(FlaskForm): 
    genre_choices = [("M", "Masculin"), ("F", "Féminin")]
    nom = StringField(
        "nom", validators=[DataRequired(), Length(min=2, max=25)]
    )
    prenom = StringField(
        "prenom", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("email", validators=[DataRequired(), Email()])
    domaine = StringField("Domaine", validators=[DataRequired()])
    adresse = StringField("ville", validators=[DataRequired()])
    date_de_naissance=DateField("date de naissance", validators=[DataRequired()])
    telephone = StringField('telephone', validators=[DataRequired()])    
    genre = SelectField("Genre", choices=genre_choices, validators=[DataRequired()])
    bio= CKEditorField("bio",render_kw={"rows": "20"},validators=[Length(max=800)])

    cv = FileField('CV', validators=[ FileAllowed(['pdf'], 'Only PDF files allowed.')])

    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Only PNG and JPEG files allowed.')])
    
    submit = SubmitField("modifier")
    #------------UpdateProfileFormrecreteur---------------
class UpdateProfileFormrecreteur(FlaskForm):
    nom_de_societe = StringField(
        "nom_de_societe ", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("email", validators=[DataRequired(), Email()])
    domaine = StringField("Domaine", validators=[DataRequired()])
    adresse = StringField("Adresse", validators=[DataRequired()])
    telephone=StringField("Telephone", validators=[DataRequired()])
    company_description= CKEditorField("company_description",render_kw={"rows": "20"})
    submit = SubmitField("modifier")
    #-------------------------------
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Recruteur.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please chosse a different one"
                )


##################
class ajouteroffreform(FlaskForm):
 titre=StringField("titre", validators=[DataRequired()])
 description = CKEditorField("description",[DataRequired()], render_kw={"rows": "20"})
 
 region = SelectField("Région", choices=[
    ( 'Sélectionnez une région'),
    ( 'Tanger-Tétouan-Al Hoceïma'),
    ( 'Oriental'),
    ( 'Fès-Meknès'),
    ( 'Rabat-Salé-Kénitra'),
    ( 'Béni Mellal-Khénifra'),
    ( 'Casablanca-Settat'),
    ( 'Marrakech-Safi'),
    ( 'Drâa-Tafilalet'),
    ( 'Souss-Massa'),
    ( 'Guelmim-Oued Noun'),
    ( 'Laâyoune-Sakia El Hamra'),
    ( 'Dakhla-Oued Ed-Dahab')
])
 diplome_requis = StringField("Diplôme requis")
 langues_requises = StringField("Langues requises")
 categories=SelectField("categories", choices=[
    ('Médical'),
    ('Technologie'),
    ('Gouvernement'),
    ('Éducation'),
    ('Finance'),
    ('Ingénierie'),
    ('Agriculture'),
    ('Art et design'),
    ('Sciences sociales'),
    ('Environnement'),
    ('Droit'),
    ('Médias et communication'),
    ('Marketing et publicité'),
    ('Ressources humaines'),
    ('Tourisme et hospitalité'),
    ('Sports et loisirs'),
    ('Transport et logistique'),
    ('Recherche scientifique'),
    ('Commerce de détail'),
    ('Fabrication'),
    ('E-commerce'),
    ('Télécommunications'),
    ('Énergie'),
    ('Immobilier'),
    ('Consultance'),
    ('Alimentation et boissons'),
    ('Mode et beauté'),
    ('Divertissement'),
    ('Musique'),
    ('Cinéma et télévision'),
    
])
 statut = StringField("Statut")
 horaire_travail = SelectField(" Horaire de travail", choices=[
    ( 'Horaire flexibles'),
    ( 'travail en journée'),
    ( 'Du lundi au vendredi'),
    ( 'Période de travail de 8 Heures'),
    ( 'Heures supplémentaires'),
    ( 'Période de travail de 10 Heures'),
    ( 'Travail les jours fériés'),
    ( 'Disponible le week-end'),
    ( 'Période de travail de 12 Heures'),
    ( 'Tous les week-ends'),
    ( 'Travail posté'),
    ( 'Week-ends uniquement'),
    ( 'Autre')
])
 slug = StringField(
    "Slug",
    validators=[ Length(max=32)],
    render_kw={
        "placeholder": "Descriptive short version of your title. SEO friendly"
    },
)
 type_de_poste=SelectField(" Type de poste", choices=[
    ( 'Temps plein'),
    ( 'CDI'),
    ( 'Intérim'),
    ( 'Temps partiel'),
    ( 'CDD'),
    ( 'Stage'),
    ( 'Alternance'),
    ( 'Indépendant/freelance'),
    ( 'Service civique'),
    ( 'Autre')
])
 salaire=StringField("salaire")
 #id_recruteur = SelectField("Recruteur", choices=[], validators=[DataRequired()])
 submit = SubmitField("ajouter offre")


class modifieroffree(ajouteroffreform):
 titre=StringField("titre")
 description = CKEditorField("description", render_kw={"rows": "20"})

 submit = SubmitField("Modifier")

##########################"
# 
