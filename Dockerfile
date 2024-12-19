# Étape 1 : Utiliser une image Python comme base
FROM python:3.11-slim

# Étape 2 : Installer SBCL pour exécuter le code Lisp
RUN apt-get update && apt-get install -y sbcl

# Étape 3 : Installer les dépendances Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4 : Copier tout le projet dans le conteneur
COPY . .

# Étape 5 : Exposer le port Flask (5000 par défaut)
EXPOSE 5000

# Étape 6 : Commande pour démarrer l'application
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
