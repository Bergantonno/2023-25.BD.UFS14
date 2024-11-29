import pytest
from app import app
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Client di test per l'app Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test: Validazione dello schema
def test_schema_validation():
    schema = {
        "type": "object",
        "properties": {
            "numeri": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 1
            }
        },
        "required": ["numeri"]
    }
    valid_data = {"numeri": [1, 2, 3]}
    invalid_data = {"numeri": "non una lista"}

    # Validazione corretta
    validate(instance=valid_data, schema=schema)

    # Validazione errata
    with pytest.raises(ValidationError):
        validate(instance=invalid_data, schema=schema)

# Test: Chiamata API con input valido
def test_api_valid_input(client, snapshot):
    input_data = {"numeri": [1, 2, 3, 4, 5]}
    response = client.post('/processa', json=input_data)
    assert response.status_code == 200

    # Snapshot del risultato
    snapshot.assert_match(response.get_json())

# Test: Chiamata API con input non valido
def test_api_invalid_input(client):
    input_data = {"valori": [1, 2, 3]}  # Chiave errata
    response = client.post('/processa', json=input_data)
    assert response.status_code == 400
    assert "errore" in response.get_json()
