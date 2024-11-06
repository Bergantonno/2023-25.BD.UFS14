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

def test_validate_user_data():
    """
    Test per validare i dati dell'utente contro uno schema JSON utilizzando jsonschema.
    """
    try:
        validate(instance=sample_data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Validation error: {e.message}")

    # Chiama la funzione validate_user_data per ulteriore verifica specifica
    result = validate_user_data(sample_data)
    assert result == True, "La funzione validate_user_data ha fallito con dati validi"

def test_invalid_user_data():
    """
    Test per controllare che la funzione validate_user_data fallisca con dati non validi.
    """
    invalid_data = sample_data.copy()
    invalid_data["age"] = "invalid_age"  # Aggiungi un valore non valido

    with pytest.raises(ValidationError):
        validate(instance=invalid_data, schema=schema)

    # Chiama la funzione validate_user_data per verificare che ritorni False
    result = validate_user_data(invalid_data)
    assert result == False, "La funzione validate_user_data ha passato dati non validi"
