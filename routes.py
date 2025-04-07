from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Blueprint
from models import db, Client
from models import db, Vehicule
from models import db, Reparation
from models import db, Intervention
from models import db, Piece
from models import db, Mecanicien

app = Flask(__name__)

app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('acceuil.html')

@app.route('/clients', methods=['GET', 'POST'])
def clients():
    result = db.session.query(
        Vehicule,
        Reparation,
        Intervention,
        Mecanicien,
        Piece
    ).join(Reparation, Vehicule.id_vehicule == Reparation.id_vehicule) \
     .join(Intervention, Reparation.id_reparation == Intervention.id_reparation) \
     .join(Mecanicien, Intervention.id_mecanicien == Mecanicien.id_mecanicien) \
     .outerjoin(Piece, Reparation.id_reparation == Piece.id_piece) \
     .all()
    
    if request.method == 'POST':
        nom = request.form['nom']
        telephone = request.form['telephone']
        email = request.form['email']
        adresse = request.form['adresse']
        immatriculation = request.form['immatriculation']
        marque = request.form['marque']
        modele = request.form['modele']
        annee = request.form['annee']

        # Création du client
        nouveau_client = Client(nom=nom, telephone=telephone, email=email, adresse=adresse)
        db.session.add(nouveau_client)
        db.session.commit()
        
        # Création du véhicule
        vehicule = Vehicule(immatriculation=immatriculation, marque=marque, modele=modele, annee=annee, id_client=nouveau_client.id_client)
        db.session.add(vehicule)
        db.session.commit()

        flash('Client et véhicule ajoutés avec succès !', 'success')
        return redirect(url_for('app.clients'))
    
    return render_template('clients.html', result=result)

@app.route('/demandes')
def demandes():
    # Modifier la requête pour utiliser 'id_client' au lieu de 'id'
    clients = db.session.query(Client, Vehicule).join(Vehicule, Client.id_client == Vehicule.id_client).all()
    return render_template('demandes.html', clients=clients)

# Route pour afficher tous les mécaniciens
@app.route('/mecaniciens')
def list_mecaniciens():
    mecaniciens = Mecanicien.query.all()  # Récupérer tous les mécaniciens
    return render_template('mecanicien.html', mecaniciens=mecaniciens)

# Route pour ajouter un mécanicien
@app.route('/mecanicien/add', methods=['GET', 'POST'])
def add_mecanicien():
    if request.method == 'POST':
        nom = request.form['nom']
        specialite = request.form['specialite']
        new_mecanicien = Mecanicien(nom=nom, specialite=specialite)
        db.session.add(new_mecanicien)
        db.session.commit()
        flash("Mécanicien ajouté avec succès!", 'success')
        return redirect(url_for('app.list_mecaniciens'))
    return render_template('add_mecanicien.html')

# Route pour mettre à jour un mécanicien
@app.route('/mecanicien/edit/<int:id>', methods=['GET', 'POST'])
def edit_mecanicien(id):
    mecanicien = Mecanicien.query.get_or_404(id)
    if request.method == 'POST':
        mecanicien.nom = request.form['nom']
        mecanicien.specialite = request.form['specialite']
        db.session.commit()
        flash("Mécanicien mis à jour avec succès!", 'success')
        return redirect(url_for('app.list_mecaniciens'))
    return render_template('edit_mecanicien.html', mecanicien=mecanicien)

# Route pour supprimer un mécanicien
@app.route('/mecanicien/delete/<int:id>', methods=['POST'])
def delete_mecanicien(id):
    mecanicien = Mecanicien.query.get_or_404(id)
    db.session.delete(mecanicien)
    db.session.commit()
    flash("Mécanicien supprimé avec succès!", 'danger')
    return redirect(url_for('app.list_mecaniciens'))

@app.route('/reponse', methods=['GET', 'POST'])
def reponse():
    if request.method == 'POST':
        date_entree = request.form['date_entree']
        date_sortie_prevue = request.form['date_sortie_prevue']
        statut = request.form['statut']
        id_vehicule = request.form['id_vehicule']

        description = request.form['description']
        cout = request.form['cout']
        duree = request.form['duree']  # Durée en minutes
        id_mecanicien = request.form['id_mecanicien']

        # Création du réparation
        nouveau_reparation = Reparation(date_entree=date_entree, date_sortie_prevue=date_sortie_prevue, statut=statut, id_vehicule=id_vehicule)
        db.session.add(nouveau_reparation)
        db.session.commit()

        # Création de intervention
        nouveau_intervention = Intervention(description=description, cout=cout, duree=duree, id_mecanicien=id_mecanicien, id_reparation=nouveau_reparation.id_reparation)
        db.session.add(nouveau_intervention)
        db.session.commit()

        flash('Réparation, pièces et intervention ajoutées avec succès !', 'success')
        return redirect(url_for('app.reponse'))

    # En mode GET, afficher le formulaire pour ajouter une réparation, des pièces et des interventions
    vehicules = Vehicule.query.all()  # Récupère tous les véhicules
    pieces = Piece.query.all()  # Récupérer toutes les pièces disponibles
    mecaniciens = Mecanicien.query.all()  # Récupérer tous les mécaniciens disponibles
    return render_template('reponse.html', pieces=pieces, mecaniciens=mecaniciens, vehicules=vehicules)


@app.route('/pieces')
def list_pieces():
    pieces = Piece.query.all()  # Récupérer toutes les pièces
    return render_template('pieces.html', pieces=pieces)

@app.route('/piece/add', methods=['GET', 'POST'])
def add_piece():
    if request.method == 'POST':
        nom = request.form['nom']
        reference = request.form['reference']
        prix = request.form['prix']
        stock = request.form['stock']
        
        new_piece = Piece(
            nom=nom, 
            reference=reference, 
            prix=prix,
            stock=stock
        )
        
        db.session.add(new_piece)
        db.session.commit()
        flash("Pièce ajoutée avec succès!", 'success')
        return redirect(url_for('app.list_pieces'))  # Redirige vers la liste des pièces

    return render_template('add_piece.html')

@app.route('/piece/edit/<int:id>', methods=['GET', 'POST'])
def edit_piece(id):
    piece = Piece.query.get_or_404(id)  # Récupérer la pièce avec l'ID, ou 404 si non trouvé
    if request.method == 'POST':
        piece.nom = request.form['nom']
        piece.reference = request.form['reference']
        piece.prix = request.form['prix']
        piece.stock = request.form['stock']
        
        db.session.commit()
        flash("Pièce mise à jour avec succès!", 'success')
        return redirect(url_for('app.list_pieces'))  # Redirige vers la liste des pièces

    return render_template('edit_piece.html', piece=piece)

@app.route('/piece/delete/<int:id>', methods=['POST'])
def delete_piece(id):
    piece = Piece.query.get_or_404(id)  # Récupérer la pièce avec l'ID, ou 404 si non trouvé
    db.session.delete(piece)  # Supprimer la pièce
    db.session.commit()
    flash("Pièce supprimée avec succès!", 'danger')
    return redirect(url_for('app.list_pieces'))  # Redirige vers la liste des pièces
