from pythonic.models import Candidat,Recruteur,OffreEmploi,Candidature
from flask import render_template, url_for, flash, redirect,session,abort,request,send_from_directory
from pythonic.forms import (RegistrationCandidat,RegistrationRecruteur, LoginForm,UpdateProfileFormcondidat,
                            ChangePasswordcondForm,UpdateProfileFormrecreteur,
                            ChangePasswordrecdForm,ajouteroffreform,modifieroffree,
                            
                            )
from pythonic import app, bcrypt,db,mail
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import send_from_directory
from flask_mail import Message
bcrypt = Bcrypt()
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from flask_bcrypt import generate_password_hash

from flask_login import current_user
from urllib.parse import unquote
from PIL import Image
import smtplib
from email.message import EmailMessage
import secrets




#-------------home---------------------------------------------------------------
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():

    offre_emploi = OffreEmploi.query.order_by(OffreEmploi.date_publication.desc()).paginate(page=1, per_page=6
    )
    #offre_emploi=OffreEmploi.query.all()
    return render_template('home.html', offre_emploi=offre_emploi)

#-----------------homecond-----------------------------------------------------------
@app.route("/")
@app.route("/homecond", methods=['GET', 'POST'])
def homecondidat():
    # Obtenez toutes les offres d'emploi lancer par les recruteures
    #offre_emploi=OffreEmploi.query.all()
    offre_emploi = OffreEmploi.query.order_by(OffreEmploi.date_publication.desc()).paginate(page=1, per_page=6
    )
    return render_template('homecondidat.html', offre_emploi=offre_emploi)

#--------------homerec---------------------
@app.route('/homerec', methods=['GET', 'POST'])
def homerecreteur():
    # Obtenez toutes les offres d'emploi du recruteur actuel
    offre_emploi = OffreEmploi.query.filter_by(recruteur_id=current_user.id_recruteur).all()
    return render_template('homerec.html', offre_emploi=offre_emploi, current_user=current_user)


#-----------update_candidature---------------
#@app.route("/update_candidature/<int:candidature_id>", methods=['POST'])
#def update_candidature(candidature_id):
  #  candidature = Candidature.query.get(candidature_id)
   # etat = request.form.get('etat')
   # candidature.etat = etat
   # db.session.commit()
   # return redirect('/homerec')
##############offre_candidats_profile###########
@app.route('/offre-candidats-profile/<int:offre_id>')
def offre_candidats_profile(offre_id):
    offre = OffreEmploi.query.filter_by(id_offre = offre_id).first()
    cc = Candidature.query.filter_by(id_offre=offre_id).all()
    candidats = []
    for c in cc:
        candidat = Candidat.query.filter_by(id_condidat=c.id_condidat).first()
        #candidats.append({'nom': candidat.nom, 'prenom': candidat.prenom, 'email': candidat.email, 'etat': c.etat})
        candidats.append(candidat)
       # candidats.append({'candidat': candidat, 'etat': c.etat})

    return render_template('details.html', user=current_user, offre=offre, candidats=candidats)

########## affichage detail de candidat "candidat_profile" ########################""

@app.route('/candidat-profile/<candidat_id>')
def candidat_profile(candidat_id):
    candidat = Candidat.query.filter_by(id_condidat=candidat_id).first()
    date_naissance = candidat.date_de_naissance
    cv_filename = secure_filename(candidat.cv)
    cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
    #form.cv.data.save(cv_path)
    profile_picture_filename = secure_filename(candidat.profile_picture)
    profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)

        #profile_picture = Image.open(os.path.abspath(c))
        #profile_picture.thumbnail((100, 100))  # Set the desired dimensions
    #resized_profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resized_' + profile_picture_filename)
        #resized_profile_picture_path = os.path.abspath(resized_profile_picture_path)
    image_file = url_for("static", filename =profile_picture_path)
    image_file = unquote(image_file).replace('/','\\').replace('user_pics_','')
        #profile_picture_path.save(resized_profile_picture_path)
    cv  = url_for("static",filename =cv_path)  
    cv = unquote(cv).replace('/','\\').replace('user_pics_','')
    return render_template('detaillescandidat.html', user=current_user, candidat=candidat,date_de_naissance=date_naissance,image_file=image_file,cv=cv )

##########affichege tout les offres f'emlpoi##################
@app.route("/")
@app.route("/offreemploi", methods=['GET', 'POST'])
def offreemploi():
    page = request.args.get("page", 1, type=int)
    offre_emploi = OffreEmploi.query.paginate(page=page, per_page=6)
    return render_template('offreemploi.html', offre_emploi=offre_emploi)

#####""""""""""""
@app.route("/")
@app.route("/offreemploic", methods=['GET', 'POST'])
def offreemploic():
    ##offre_emploi=OffreEmploi.query.all()
    page = request.args.get("page", 1, type=int)
    offre_emploi = OffreEmploi.query.paginate(page=page, per_page=6)
    return render_template('offreemploic.html', offre_emploi=offre_emploi)

#------------inscriptioncond----------------------------------------------------------------
import os
from werkzeug.utils import secure_filename
@app.route('/inscription/candidat', methods=['GET', 'POST'])
def inscription_candidat():
    form = RegistrationCandidat()
    resized_profile_picture_path = None
    image_file = None
    xcv = 1000
    if form.validate_on_submit():
           # Hashage du mot de passe
        cv_filename = secure_filename(form.cv.data.filename)
        cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
        form.cv.data.save(cv_path)

        profile_picture_filename = secure_filename(form.profile_picture.data.filename)
        profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)

        #profile_picture = Image.open(os.path.abspath(c))
        #profile_picture.thumbnail((100, 100))  # Set the desired dimensions
        resized_profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resized_' + profile_picture_filename)
        #resized_profile_picture_path = os.path.abspath(resized_profile_picture_path)
        image_file = url_for("static", filename =profile_picture_path)
        #profile_picture_path.save(resized_profile_picture_path)
        
        form.profile_picture.data.save(resized_profile_picture_path)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        #datetime.strptime(date_str, '%Y-%m-%d')
        date_de_naissance=form.date_naissance.data
        print('hahah',os.path.abspath(resized_profile_picture_path))
        max_id_condidat = db.session.query(db.func.max(Candidat.id_condidat)).scalar()
        if max_id_condidat is None:
            max_id_condidat = 999
        candidat =Candidat(
            id_condidat=max_id_condidat+1,
            nom=form.nom.data,
            prenom=form.prenom.data,
            email=form.email.data,
            date_de_naissance=datetime.strptime(date_de_naissance, '%Y-%m-%d'),
            mot_de_passe=hashed_password,
            domaine=form.domaine.data,
            telephone=form.telephone.data,
            adresse=form.adresse.data,
            cv=cv_path,
            profile_picture = resized_profile_picture_path,
            )
        db.session.add(candidat)
        db.session.commit()
        flash("Compte créé avec succès. Vous pouvez maintenant vous connecter.")
        # Traitement des données du formulaire et enregistrement du candidat
        return redirect(url_for('login'))
        
    return render_template('InscriptionCandidat.html', title="RegistrationCandidat", image_file=image_file ,image_path=resized_profile_picture_path,form=form)


#------------inscriptionrec----------------------------------------------------------------
@app.route('/inscription/recruteur', methods=['GET', 'POST'])
def inscription_recruteur():
    form = RegistrationRecruteur()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        recreteur= Recruteur(
        nom_de_societe=form.nom_societe.data,
        adresse=form.adresse.data,
        email=form.email.data,
        mot_de_passe=hashed_password,
        domaine=form.domaine.data,
        telephone=form.telephone.data
)
        db.session.add( recreteur)
        db.session.commit()
        flash("Compte créé avec succès. Vous pouvez maintenant vous connecter.")
        return redirect(url_for("login"))
    return render_template('inscriptionRecruteur.html', title="RegistrationRecruteur",form=form)
#----------login------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
     email = form.email.data
     password = form.password.data
     remember = form.remember.data
    candidat = Candidat.query.filter_by(email=form.email.data).first()
    if candidat and bcrypt.check_password_hash(candidat.mot_de_passe, form.password.data):
        login_user(candidat, remember=remember)
        flash('Bienvenue dans votre profil {}'.format(current_user.nom,current_user.prenom))

        return redirect(url_for('homecondidat'))
    recruteur = Recruteur.query.filter_by(email=form.email.data).first()
    if recruteur and bcrypt.check_password_hash(recruteur.mot_de_passe, form.password.data):
           login_user(recruteur, remember=remember)
           flash('Bienvenue dans votre profil {}'.format(current_user.nom_de_societe))
           return redirect(url_for('homerecreteur'))
   

    return render_template('login.html', form=form)

#---------dashboardcond-------------------------------------------------------------------

@app.route("/dashboardcond", methods=["GET"])
@login_required
def dashboardcond():
     
    return render_template("dashboardcond.html", title="dashboardcond", active_tab=None)
#---------dashboardrec-------------------------------------------------------------------
@app.route("/dashboardrec", methods=["GET"])
@login_required
def dashboardrec():
    return render_template("dashboardRecreteur.html", title="dashboardrec", active_tab=None)


#######A propos de nous#########"
# 
@app.route("/apropos", methods=["GET"])

def apropos():
     return render_template("propo.html", title="propo")
#------------dashboarprofil les information de candidat pour faire modification----------------------------------------------------------------
@app.route("/dashboard/profilc", methods=["GET", "POST"])
@login_required
def dashboard_candidat():
    profile_form = UpdateProfileFormcondidat()

    if profile_form.validate_on_submit():
        cv_filename = None
        if profile_form.cv.data:
            cv_filename = secure_filename(profile_form.cv.data.filename)
            cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
            profile_form.cv.data.save(cv_path)
        
        profile_picture_filename = None
        if profile_form.profile_picture.data:
            profile_picture_filename = secure_filename(profile_form.profile_picture.data.filename)
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
            resized_profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resized_' + profile_picture_filename)
            
            profile_form.profile_picture.data.save(resized_profile_picture_path)
        #modif de profil
        current_user.nom = profile_form.nom.data
        current_user.prenom = profile_form.prenom.data
        current_user.email = profile_form.email.data
        current_user.domaine = profile_form.domaine.data
        current_user.adresse = profile_form.adresse.data
        current_user.date_de_naissance = profile_form.date_de_naissance.data
        current_user.genre = profile_form.genre.data
        current_user.bio = profile_form.bio.data
        current_user.telephone = profile_form.telephone.data
        
        if cv_filename:
            current_user.cv = cv_path
        if profile_picture_filename:
            current_user.profile_picture = resized_profile_picture_path
        
        db.session.commit()
        flash("Votre profil a été modifié avec succès.", "success")
        return redirect(url_for("dashboardcond"))

    profile_form.profile_picture.data = current_user.profile_picture
    profile_form.cv.data = current_user.cv
    profile_form.nom.data = current_user.nom
    profile_form.prenom.data = current_user.prenom
    profile_form.email.data = current_user.email
    profile_form.domaine.data = current_user.domaine
    profile_form.adresse.data = current_user.adresse
    profile_form.date_de_naissance.data = current_user.date_de_naissance
    profile_form.genre.data = current_user.date_de_naissance
    profile_form.bio.data = current_user.bio
    profile_form.telephone.data = current_user.telephone

    cv_content = url_for("static", filename=f'{current_user.cv}')
    cv_content = unquote(cv_content)

    image_file = url_for("static", filename=f'{current_user.profile_picture}')
    image_file = unquote(image_file)

    return render_template("updateprofilcondidat.html", title="Candidat Dashboard", profile_form=profile_form, cv=cv_content, image_file=image_file)

#------------dashboarprofil modif les information de recreteur----------------------------------------------------------------
@app.route("/dashboard/profilr", methods=["GET", "POST"])
@login_required
def modifierprofil_rec():
 profile_form =  UpdateProfileFormrecreteur()
 if profile_form.validate_on_submit():
        current_user.nom_de_societe = profile_form.nom_de_societe.data
        current_user.email = profile_form.email.data
        current_user.domaine = profile_form.domaine.data
        current_user.adresse = profile_form.adresse.data
        current_user.telephone=profile_form.telephone.data
        current_user.company_description=profile_form.company_description.data
        db.session.commit()
        flash("votre profil a été modifié avec succés.", "success")
        return redirect(url_for("dashboardrec"))
 profile_form.nom_de_societe.data = current_user.nom_de_societe 
 profile_form.email.data = current_user.email
 profile_form.domaine.data = current_user.domaine
 profile_form.adresse.data = current_user.adresse
 profile_form.telephone.data=current_user.telephone
 profile_form.company_description.data=current_user.company_description


 return render_template("updateprofilrec.html", title="recreteur Dashboard",profile_form=profile_form)


#----------logout------------------------------------------------------------------
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
#------------changerpassword candidat----------------------------------------------------------------
@app.route('/change_passwordc', methods=['GET', 'POST'])
@login_required
def change_passwordc():
    form = ChangePasswordcondForm()
    if form.validate_on_submit():
        user0 = current_user
        print(user0.id_condidat)
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
       
        user1 = Candidat.query.get(user0.id_condidat)
        user1.mot_de_passe = hashed_password

        print(user1.nom)
        try :
            db.session.commit()
            flash('Le mot de passe a été changé avec succès!', 'success')
        except :
            flash('db not', 'danger')
         
        return redirect(url_for('dashboardcond'))
    
    return render_template('Security.html', form=form)


from flask import flash, redirect, url_for

#------------changerpassword recreteur----------------------------------------------------------------
@app.route('/change_passwordr', methods=['GET', 'POST'])
@login_required
def change_passwordr():
    form = ChangePasswordrecdForm()
    if form.validate_on_submit():
        user0 = current_user
        print(user0.id_recruteur)
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
       
        user1 = Recruteur.query.get(user0.id_recruteur)
        user1.mot_de_passe = hashed_password

        
        try :
            db.session.commit()
            flash('Le mot de passe a été changé avec succès!', 'success')
        except :
            flash('db not', 'danger')
       
        return redirect(url_for('dashboardrec'))
    
    return render_template('Securityrec.html', form=form)


from flask import flash, redirect, url_for

###########################"
@app.route("/delete-account")
@login_required
def delete_account():
    if isinstance(current_user, Candidat):
        # Delete candidatures associated with the current_user
        for candidature in current_user.candidatures:
            db.session.delete(candidature)
    elif isinstance(current_user, Recruteur):
        # Delete offers and associated candidatures
        for offre in current_user.offres:
            for candidature in offre.candidatures:
                db.session.delete(candidature)
            db.session.delete(offre)

    # Delete the current_user
    db.session.delete(current_user)
    db.session.commit()

    logout_user()

    return redirect(url_for("home"))

######################


######################ajouter offre###########
      
@app.route("/ajouter_offre", methods=["GET", "POST"])
@login_required
def ajouter_offre():
    newOffrerec_form = ajouteroffreform()

    if newOffrerec_form.validate_on_submit():

        offre = OffreEmploi(
            titre=newOffrerec_form.titre.data,
            description=newOffrerec_form.description.data,
            region=newOffrerec_form.region.data,
            diplome_requis=newOffrerec_form.diplome_requis.data,
            langues_requises=newOffrerec_form.langues_requises.data,
            categories=newOffrerec_form.categories.data,
            statut=newOffrerec_form.statut.data,
            horaire_travail=newOffrerec_form.horaire_travail.data,
            slug=newOffrerec_form.slug.data,
            type_de_poste=newOffrerec_form.type_de_poste.data,
            salaire=newOffrerec_form.salaire.data,
            recruteur_id = current_user.id_recruteur
        )

        db.session.add(offre)
        db.session.commit()

        flash("Votre offre a été créée avec succès!", 'success')
        return redirect(url_for("dashboardrec"))

    return render_template("newOffrerec.html", title="Nouvelle offre", newOffrerec_form=newOffrerec_form)


    #################################################""


#""""affichege d'offre ######################""
@app.route("/offre-profile/<string:offre_title>")
def offre(offre_title):
    offre = OffreEmploi.query.filter_by(titre=offre_title).first()
    offre_id = offre.id_offre if offre else None
    offre = OffreEmploi.query.get_or_404(offre_id )
    return render_template("offre.html",title=offre.titre,offre=offre,current_user=current_user )
#########################################
@app.route("/offre-profilec/<string:offre_title>")
def offrec(offre_title):
    offre = OffreEmploi.query.filter_by(titre=offre_title).first()
    offre_id = offre.id_offre if offre else None
    offre = OffreEmploi.query.get_or_404(offre_id )
    return render_template("offrec.html",title=offre.titre,offre=offre,current_user=current_user )

##############affichage d'offre recreteur###############################"
@app.route("/offre-profilerec/<string:offre_title>")
def offrerec(offre_title):
    offrerec = OffreEmploi.query.filter_by(titre=offre_title).first()
    offre_id = offrerec.id_offre if offrerec else None
    offrerec = OffreEmploi.query.get_or_404(offre_id )
    return render_template("offrerec.html",title=offrerec.titre,offrerec=offrerec,current_user=current_user )

##############afficher mey offre#####################
@app.route("/myoffre", methods=["GET", "POST"])
@login_required
def user_offre():
    page = request.args.get("page", 1, type=int)
    #offre_emploi = OffreEmploi.query.paginate(page=page, per_page=6)
    offre_emploi = OffreEmploi.query.filter_by(recruteur_id=current_user.id_recruteur).paginate(page=page, per_page=6)

    return render_template("myoffre.html", title="mes offres", active_tab="user_offre", current_user=current_user, offre_emploi=offre_emploi)

######################Modifier l'offre##############
@app.route("/offre-profile/<string:offre_title>/modifieroffre",methods=["GET", "POST"])
def modifieroffre(offre_title):
    offre = OffreEmploi.query.filter_by(titre=offre_title).first()
    offre_id = offre.id_offre if offre else None
    offre = OffreEmploi.query.get_or_404(offre_id )
    form = modifieroffree()
    if form.validate_on_submit():
        offre.titre = form.titre.data
        offre.description = form.description.data
        offre.slug = str(form.slug.data).replace(" ", "-")
        offre.region = form.region.data
        offre.diplome_requis = form.diplome_requis.data
        offre.langues_requises = form.langues_requises.data
        offre.categories = form.categories.data
        offre.statut = form.statut.data
        offre.horaire_travail = form.horaire_travail.data
        offre.type_de_poste= form.type_de_poste.data
        offre.salaire = form.salaire.data
        db.session.commit()
        flash("votre offre modifier", "success")
        return redirect(url_for('offrerec', offre_title=offre.titre))
    elif request.method == "GET":
        form.titre.data = offre.titre
        form.description.data= offre.description
        form.slug.data = offre.slug
        form.region.data = offre.region
        form.diplome_requis.data = offre.diplome_requis
        form.langues_requises.data = offre.langues_requises
        form.categories.data = offre.categories
        form.statut.data = offre.statut
        form.horaire_travail.data = offre.horaire_travail
        form.type_de_poste.data = offre.type_de_poste
        form.salaire.data = offre.salaire
    
    return render_template("modifieroffre.html",title="Update |"+offre.titre,offre=offre,current_user=current_user,form=form )



####################postuler offre#######################
@app.route('/postuler/<int:offre_id>', methods=['POST'])
def postuler(offre_id):
    if not current_user.is_authenticated:
        flash("Vous devez vous connecter pour postuler à cette offre", "danger")
        return redirect(url_for('login'))

    offre = OffreEmploi.query.get(offre_id)
    if not offre:
        flash("L'offre d'emploi n'existe pas", "danger")
        return redirect(url_for('home'))
    existing_candidature = Candidature.query.filter_by(
        id_offre=offre_id,
        id_condidat=current_user.id_condidat
    ).first()
    if existing_candidature:
        flash("Vous avez déjà postulé à cette offre", "danger")
        return redirect(url_for('homecondidat'))
    candidature = Candidature(
        id_offre=offre_id,
        id_condidat=current_user.id_condidat,etat = 'En Attente')
    db.session.add(candidature)
    db.session.commit()
    flash("Votre candidature a été soumise avec succès", "success")
    return redirect(url_for('homecondidat'))

########################supprimer offre##############
@app.route('/offres/annuler/<offre_id>')
def offres_annuler(offre_id):
    offre = OffreEmploi.query.filter_by(id_offre=offre_id).first()
    postulations = Candidature.query.filter_by(id_offre=offre.id_offre).all()
    db.session.delete(offre)

    for p in postulations:
        db.session.delete(p)

    db.session.commit()
    flash('Cette offre a été supprimée', category='success')
    return redirect('/homerec')
##########################################
@app.route('/search', methods=['GET'])
def search_offres():
    categories = request.args.get('categories')
    title = request.args.get('title')
    region = request.args.get('region')
    
    query = OffreEmploi.query
    
    if categories:
        query = query.filter_by(categories=categories)

    if title:
        query = query.filter(OffreEmploi.titre.ilike(f'%{title}%'))

    if region:
        query = query.filter_by(region=region)
        
    page = request.args.get("page", 1, type=int)
    per_page = 6  # Nombre d'offres par page
    
    offres = query.paginate(page=page, per_page=per_page)

    return render_template('search_results.html', offres=offres)


####afficher mes candidature
@app.route('/mescandidatures')
@login_required
def mesCandidatures():
  candidatures = Candidature.query.filter_by(id_condidat=current_user.id_condidat).all()
  return render_template('condidature.html',current_user=current_user, candidatures=candidatures)
##################################



#####"""""""""""
# 
@app.route('/searchc', methods=['GET'])
def search_offresc():
    categories = request.args.get('categories')
    title = request.args.get('title')
    region = request.args.get('region')
    query = OffreEmploi.query
    if categories:
        query = query.filter_by(categories=categories)

    if title:
        query = query.filter(OffreEmploi.titre.ilike(f'%{title}%'))
    if region:
        query = query.filter_by(region=region)

    page = request.args.get("page", 1, type=int)
    per_page = 6  
    offres = query.paginate(page=page, per_page=per_page)

    return render_template('search_resultsc.html', offres=offres)


##############################
def envoie_email(receiver, subject, message):
    sender_email = "fadwamekayssi7@gmail.com"
    password = "ykhgesnojakbtvhv"

    email = EmailMessage()
    email["From"] = sender_email
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")
    server.send_message(email)
    print("Email has been sent to", receiver)
    server.quit()


import string
import secrets

def generer_mdp(length):
    characters = string.ascii_letters + string.digits + "@*^%$#!"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

#from flask_bcrypt import generate_password_hash

@app.route('/oublier_mot_de_passe', methods=['GET', 'POST'])
def oubliermdp():

    if request.method == 'POST':
        email = request.form.get('email')

        candidat = Candidat.query.filter_by(email=email).first()
        recruteur = Recruteur.query.filter_by(email=email).first()
        mot_de_passe = generer_mdp(8)

        if candidat:
            candidat.mot_de_passe = generate_password_hash(mot_de_passe)
            envoie_email(candidat.email, 'Voila votre mot de passe', 'Voici votre nouveau mot de passe : ' +mot_de_passe)
            flash('Votre nouveau mot de passe a été envoyé par e-mail', category='success')
            db.session.commit()
            return redirect('/login')

        elif recruteur:
            recruteur.mot_de_passe = generate_password_hash(mot_de_passe)
            envoie_email(recruteur.email, 'Voila votre mot de passe', 'Voici votre nouveau mot de passe : ' + mot_de_passe)
            flash('Votre nouveau mot de passe a été envoyé par e-mail', category='success')
            db.session.commit()
            return redirect('/login')

        else:
            flash('Email n\'existe pas. Créez un nouveau compte', category='danger')

    return render_template("reset_request.html")
