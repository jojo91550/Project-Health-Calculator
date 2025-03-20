FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les packages
COPY requirements.txt .

# Mettre à jour requirements.txt pour inclure gunicorn
RUN echo "gunicorn==20.1.0" >> requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY health-calculator-service/app.py health-calculator-service/health_utils.py ./

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 5000

# Commande pour démarrer l'application avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]