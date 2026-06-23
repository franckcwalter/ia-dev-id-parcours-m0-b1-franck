import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_predict_valid(client):
    response = client.post("/predict", json={
        "type_machine": "compresseur",
        "age_machine_jours": 1500,
        "derniere_maintenance_jours": 45,
        "temperature_moyenne": 68.5,
        "vibration_moyenne": 3.2,
        "pression_moyenne": 7.8,
        "nb_incidents_3_mois": 2
    })
    assert response.status_code == 200
    body = response.json()
    assert body["criticite"] in {"basse","moyenne","haute"}
    assert abs(sum(body["probabilites"].values()) - 1.0) < 1e-6

def test_predict_invalid(client):
    response = client.post("/predict", json={
        "type_machine": "INCONNU",
        "age_machine_jours": 1500,
        "derniere_maintenance_jours": 45,
        "temperature_moyenne": 68.5,
        "vibration_moyenne": 3.2,
        "pression_moyenne": 7.8,
        "nb_incidents_3_mois": 2
    })
    assert response.status_code == 422


@pytest.mark.parametrize("type_machine", ["pompe", "convoyeur", "presse", "four"])
def test_predict_parametrized(client,type_machine ):
    response = client.post("/predict", json={
        "type_machine": type_machine,
        "age_machine_jours": 1500,
        "derniere_maintenance_jours": 45,
        "temperature_moyenne": 68.5,
        "vibration_moyenne": 3.2,
        "pression_moyenne": 7.8,
        "nb_incidents_3_mois": 2
    })
    assert response.status_code == 200
