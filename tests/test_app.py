import pytest
import json
from snapshottest import Snapshot

# Test dell'API usando pytest
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
