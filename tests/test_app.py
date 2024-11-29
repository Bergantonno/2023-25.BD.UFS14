import pytest
import json
import importlib.util
from snapshottest import Snapshot

# Carica dinamicamente l'app da un file esterno
def carica_modulo(file_path, nome_modulo):
    spec = importlib.util.spec_from_file_location(nome_modulo, file_path)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

# Carichiamo il modulo 'app.py'
app = carica_modulo('app.py', 'app')

# Test dell'API usando pytest
@pytest.fixture
def client():
    app_instance = app.app
    app_instance.testing = True
    return app_instance.test_client()

def test_processa_endpoint(client, snapshot):
    # Dati di input
    dati = {"numeri": [2, 3, 4, 5, 6, 7, 8, 9]}
    
    # Chiamata all'endpoint
    response = client.post("/processa", data=json.dumps(dati), content_type="application/json")
    
    # Verifica del codice di stato
    assert response.status_code == 200
    
    # Verifica della risposta
    risultato = response.get_json()
    snapshot.assert_match(risultato, "risultato_atteso")

def test_html_serving(client):
    # Testa se l'HTML viene servito correttamente
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Analisi dei Numeri</title>" in response.data
