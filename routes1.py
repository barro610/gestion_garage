from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask import Blueprint

app = Flask(__name__)

routes_bp = Blueprint('routes', __name__)

# Page d'inscription
@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Vérifier si l'email est déjà utilisé
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Cet email est déjà utilisé. Veuillez vous connecter.', 'error')
            return redirect(url_for('routes.login'))  # Rediriger vers la page de connexion
        
        password_hash = generate_password_hash(password)
        
        # Créer un nouvel utilisateur
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('routes.login'))  # Rediriger vers la page de connexion
    
    return render_template('register.html')

# Page de connexion
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id  # Crée une session pour l'utilisateur connecté
            if user.role == 'admin':
                return redirect(url_for('routes.admin_home'))
            else:
                return redirect(url_for('routes.user_home'))
        else:
            flash('Identifiants incorrects', 'danger')
            return redirect(url_for('routes.login'))
    
    return render_template('login.html')

# Page d'accueil pour les admins
@routes_bp.route('/admin')
def admin_home():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))  # Redirige vers la page de connexion si non connecté
    user = User.query.get(session['user_id'])
    if user.role == 'admin':
        return render_template('admin.html')
    return redirect(url_for('routes.user_home'))  # Si ce n'est pas un admin, redirection vers la page utilisateur

# Page d'accueil pour les utilisateurs
@routes_bp.route('/user')
def user_home():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))  # Redirige vers la page de connexion si non connecté
    user = User.query.get(session['user_id'])
    if user.role == 'user':
        return redirect(url_for('app.clients'))  # Page utilisateur
    return redirect(url_for('routes.admin_home'))  # Si ce n'est pas un utilisateur, redirection vers la page admin


# Déconnexion
@routes_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Supprime l'id de l'utilisateur de la session
    flash('Déconnexion réussie!', 'success')
    return redirect(url_for('app.home'))