import sys
import os
from flask import Flask, render_template

# Ajouter les chemins nécessaires au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

# Importer le Blueprint des routes
from backend.routes.api_routes import api_bp

# Création de l'application Flask
app = Flask(__name__, template_folder='frontend/templates')

# Enregistrer le Blueprint pour les routes API
app.register_blueprint(api_bp, url_prefix='/api')

# Route pour le frontend
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
