from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from routes import app as routes_app  # Import des routes enregistrées dans routes.py
from routes1 import routes_bp
from models import db  # Import de l'instance de SQLAlchemy

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement des configurations
app.config.from_object(Config)

# Configuration de la base de données et des migrations
db.init_app(app)
migrate = Migrate(app, db)

# Enregistrement des blueprints (routes définies dans routes.py)
app.register_blueprint(routes_app)
app.register_blueprint(routes_bp)

# Point d'entrée pour exécuter l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
