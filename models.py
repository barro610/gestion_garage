from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Client(db.Model):
    id_client = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    adresse = db.Column(db.String(200))
    
    vehicules = db.relationship('Vehicule', backref='client', lazy=True)

class Vehicule(db.Model):
    id_vehicule = db.Column(db.Integer, primary_key=True)
    immatriculation = db.Column(db.String(20), unique=True, nullable=False)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'), nullable=False)
    
    reparations = db.relationship('Reparation', backref='vehicule', lazy=True)

class Reparation(db.Model):
    id_reparation = db.Column(db.Integer, primary_key=True)
    date_entree = db.Column(db.Date, nullable=False)
    date_sortie_prevue = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(50), nullable=False)
    id_vehicule = db.Column(db.Integer, db.ForeignKey('vehicule.id_vehicule'), nullable=False)
    
    interventions = db.relationship('Intervention', backref='reparation', lazy=True)

class Piece(db.Model):
    id_piece = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    reference = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Intervention(db.Model):
    id_intervention = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    cout = db.Column(db.Float, nullable=False)
    duree = db.Column(db.Integer, nullable=False)  # Durée en minutes
    id_reparation = db.Column(db.Integer, db.ForeignKey('reparation.id_reparation'), nullable=False)
    id_mecanicien = db.Column(db.Integer, db.ForeignKey('mecanicien.id_mecanicien'), nullable=False)
    
class Mecanicien(db.Model):
    id_mecanicien = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')  # admin ou user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)