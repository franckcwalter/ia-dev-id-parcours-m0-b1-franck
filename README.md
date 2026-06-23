# Maintenance prédictive — API de criticité

Service REST qui expose un modèle scikit-learn de classification de criticité
machine (basse / moyenne / haute) via FastAPI.

## Démarrage avec Docker

Prérequis : [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et démarré.

```bash
# Construire l'image
docker build -t fastia-maintenance:dev .

# Lancer le conteneur et mapper le port 8000
docker run --rm -p 8000:8000 fastia-maintenance:dev
```

L'API écoute sur <http://localhost:8000>. Swagger est sur `/docs`, et `/health`
renvoie `{"status": "ok", "model_loaded": true}` une fois le modèle chargé.

## Routes

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/health` | Statut du service et chargement du modèle |
| `POST` | `/predict` | Prédit la criticité d'une machine |
| `GET` | `/docs` | Documentation Swagger interactive |

Le détail des champs attendus par `/predict` est disponible dans Swagger.

## Tester l'API

Vérifier que le service répond :

```bash
# Santé du service
curl http://localhost:8000/health
```

Demander une prédiction :

```bash
# Criticité d'une machine
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "type_machine": "compresseur",
    "age_machine_jours": 1500,
    "derniere_maintenance_jours": 45,
    "temperature_moyenne": 68.5,
    "vibration_moyenne": 3.2,
    "pression_moyenne": 7.8,
    "nb_incidents_3_mois": 2
  }'
```

## Logs

Chaque appel à `/predict` est journalisé via Loguru : le payload reçu et la
durée de la prédiction. Les logs partent dans la console et dans
`logs/api.log` (rotation à 5 Mo, rétention 7 jours, archives compressées).

## Tests unitaires

Les tests couvrent les deux routes via le `TestClient` de FastAPI :
`tests/test_health.py` (santé du service) et `tests/test_predict.py`
(cas valide, entrée invalide → 422, et chaque type de machine).

```bash
# Toute la suite
pytest

# Seulement les tests de /health
pytest tests/test_health.py -v

# Seulement les tests de /predict
pytest tests/test_predict.py -v
```