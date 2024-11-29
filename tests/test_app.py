import pytest
import json
import importlib
from snapshottest import Snapshot
from app import processa_numeri

@pytest.fixture
def snapshot(snapshot: Snapshot):
    return snapshot

def test_processa_numeri(snapshot):
    # Input di esempio
    numeri_input = [1, 2, 3, 4, 5]
    # Chiamata alla funzione
    risultato = processa_numeri({"numeri": numeri_input})
    # Aspettarsi l'output in formato JSON
    expected = {
        "numeri": numeri_input,
        "somma": 15,
        "numeri_pari": [2, 4],
        "numeri_dispari": [1, 3, 5],
        "numeri_primi": [2, 3, 5]
    }
    # Verifica con lo snapshot
    snapshot.assert_match(risultato, "processa_numeri_snapshot")
    # Test aggiuntivo diretto
    assert risultato == expected
