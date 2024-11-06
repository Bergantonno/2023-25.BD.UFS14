import jsonschema
from jsonschema import validate

# Definiamo lo schema JSON
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "email": {"type": "string", "format": "email"},
    },
    "required": ["name", "age", "email"]
}

def validate_user_data(data):
    """
    Valida i dati JSON in base allo schema fornito.
    """
    try:
        validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        return False
