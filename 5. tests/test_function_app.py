import pytest
import json
from function_app import validate_user_data
import jsonschema
from jsonschema import validate, ValidationError

# Carica dati di esempio e schema
with open("tests/test_data.json") as f:
    sample_data = json.load(f)

with open("tests/schema.json") as f:
    schema = json.load(f)

def test_validate_user_data(snapshot):
    """
    Test per validare i dati dell'utente contro uno schema JSON
    e verificare che i dati restituiti siano invariati tramite snapshot.
    """
    # Valida il JSON contro lo schema
    try:
        validate(instance=sample_data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Validation error: {e.message}")

    # Chiama la funzione validate_user_data e verifica il risultato
    result = validate_user_data(sample_data)
    assert result == True, "La funzione validate_user_data ha fallito con dati validi"

    # Confronta lo snapshot con i dati di esempio
    snapshot.assert_match(sample_data, "sample_data_snapshot")

def test_invalid_user_data(snapshot):
    """
    Test per controllare che la funzione validate_user_data fallisca con dati non validi
    e validazione snapshot.
    """
    invalid_data = sample_data.copy()
    invalid_data["age"] = "invalid_age"  # Aggiungi un valore non valido

    with pytest.raises(ValidationError):
        validate(instance=invalid_data, schema=schema)

    # Verifica che la funzione ritorni False per dati non validi
    result = validate_user_data(invalid_data)
    assert result == False, "La funzione validate_user_data ha passato dati non validi"

    # Confronta lo snapshot con i dati non validi
    snapshot.assert_match(invalid_data, "invalid_data_snapshot")
