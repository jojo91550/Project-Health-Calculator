# Health Calculator Microservice

Un microservice Python qui calcule des métriques de santé (IMC et MB) via une API REST. Projet conteneurisé avec Docker, géré avec Makefile, et prêt pour le déploiement sur Azure.

## Fonctionnalités

- **Calcul d'IMC (Indice de Masse Corporelle)**
  - Formule utilisée: `IMC = poids (kg) / (taille (m))²`
  - Catégorisation (Insuffisance pondérale, Normal, Surpoids, Obésité)

- **Calcul de MB (Métabolisme de Base)** selon l'équation de Harris-Benedict
  - Pour les hommes: `MB = 88.362 + (13.397 × poids en kg) + (4.799 × taille en cm) - (5.677 × âge en années)`
  - Pour les femmes: `MB = 447.593 + (9.247 × poids en kg) + (3.098 × taille en cm) - (4.330 × âge en années)`

- **Interface utilisateur web**
  - Formulaires pour calculer l'IMC et le MB directement dans le navigateur
  - Documentation des API intégrée

## Structure du projet

```
health-calculator-service/
├── app.py              # Application Flask avec endpoints et interface utilisateur
├── health_utils.py     # Fonctions utilitaires pour les calculs
└── test.py             # Tests unitaires

Dockerfile              # Configuration Docker (à la racine)
Makefile                # Automatisation des tâches (à la racine)
requirements.txt        # Dépendances du projet (à la racine)
```

## Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Docker (pour la conteneurisation)
- Git (pour le versionnement)

## Installation et utilisation

### 1. Création de l'environnement virtuel Python

Avant d'installer les dépendances, il est recommandé de créer un environnement virtuel Python pour isoler votre projet:

```bash
# Création de l'environnement virtuel
python3 -m venv .venv

# Activation de l'environnement virtuel (Windows)
.venv\Scripts\activate

# Activation de l'environnement virtuel (Linux/macOS)
source .venv/bin/activate
```

Vous saurez que l'environnement virtuel est activé quand vous verrez `(.venv)` au début de votre ligne de commande.

### 2. Installation des dépendances

Une fois l'environnement virtuel activé:

```bash
make init
```

### 3. Exécuter les tests

```bash
make test
```

### 4. Lancer l'application en mode développement

```bash
make run
```

L'application sera accessible à l'adresse http://localhost:5000

### 5. Construction de l'image Docker

```bash
make build
```

### 6. Exécuter l'application dans un conteneur Docker

```bash
make docker-run
```

L'application conteneurisée sera accessible à l'adresse http://localhost:5000

### 7. Arrêter le conteneur Docker

```bash
make docker-stop
```

### 8. Nettoie les fichiers temporaires et compilés

```bash
make clean
```

### 9. Désactivation de l'environnement virtuel

Lorsque vous avez terminé de travailler sur le projet:

```bash
deactivate
```

## Commandes du Makefile

| Commande | Description |
|----------|-------------|
| `make init` | Installe les dépendances nécessaires |
| `make run` | Lance l'application en mode développement |
| `make test` | Exécute les tests unitaires |
| `make build` | Construit l'image Docker |
| `make docker-run` | Lance l'application dans un conteneur Docker |
| `make docker-stop` | Arrête le conteneur Docker |
| `make clean` | Nettoie les fichiers temporaires et compilés |

## Utilisation des API

### Calcul de l'IMC

**Endpoint**: `/bmi` (POST)

**Corps de la requête**:
```json
{
  "height": 1.75,  // Taille en mètres
  "weight": 70     // Poids en kilogrammes
}
```

**Exemple avec curl**:
```bash
curl -X POST http://localhost:5000/bmi \
  -H "Content-Type: application/json" \
  -d '{"height": 1.75, "weight": 70}'
```

**Réponse**:
```json
{
  "bmi": 22.86,
  "category": "Normal weight"
}
```

### Calcul du MB

**Endpoint**: `/bmr` (POST)

**Corps de la requête**:
```json
{
  "height": 175,     // Taille en centimètres
  "weight": 70,      // Poids en kilogrammes
  "age": 30,         // Âge en années
  "gender": "male"   // Genre: "male" ou "female"
}
```

**Exemple avec curl**:
```bash
curl -X POST http://localhost:5000/bmr \
  -H "Content-Type: application/json" \
  -d '{"height": 175, "weight": 70, "age": 30, "gender": "male"}'
```

**Réponse**:
```json
{
  "bmr": 1695.67,
  "unit": "calories/day"
}
```

## Tests

Le projet inclut des tests unitaires pour les fonctions principales:
- Tests des calculs d'IMC
- Tests des calculs de MB pour hommes et femmes

Les tests peuvent être exécutés avec la commande `make test`.

## Prochaines étapes

- CI/CD Pipeline avec GitHub Actions
- Déploiement sur Azure App Service
