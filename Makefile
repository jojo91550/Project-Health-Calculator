# Installer les dépendances
init:
	@echo "Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Exécuter l'application Flask
run:
	@echo "Running the Flask app..."
	cd health-calculator-service && python app.py

# Exécuter les tests
test:
	@echo "Running tests..."
	cd health-calculator-service && \
	pip install pytest && \
	python -m unittest test.py

# Construire l'image Docker
build:
	@echo "Building the Docker image..."
	docker build -t health-calculator:latest .

# Exécuter le conteneur Docker
docker-run:
	@echo "Running the Docker container..."
	docker run -d -p 5000:5000 --name health-calculator health-calculator:latest
	@echo "Service started at http://localhost:5000"

# Arrêter le conteneur Docker
docker-stop:
	@echo "Stopping the Docker container..."
	docker stop health-calculator || true
	docker rm health-calculator || true

# Nettoyer l'environnement
clean:
	@echo "Cleaning up..."
	cd health-calculator-service && \
	find . -type d -name __pycache__ -exec rm -rf {} + && \
	find . -type f -name "*.pyc" -delete