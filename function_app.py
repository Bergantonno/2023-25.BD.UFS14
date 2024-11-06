import json
import azure.functions as func
from jsonschema import validate, ValidationError

# Definisci lo schema per la validazione JSON
user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"]
}

def validate_user_data(data):
    """
    Funzione per validare i dati JSON di un utente.
    Restituisce True se i dati sono validi, altrimenti False.
    """
    try:
        validate(instance=data, schema=user_schema)
        return True
    except ValidationError:
        return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Funzione Azure che riceve una richiesta HTTP contenente dati JSON,
    li valida e restituisce una risposta.
    """
    try:
        # Ottieni i dati JSON dalla richiesta
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Richiesta non valida: il corpo della richiesta deve essere JSON.",
            status_code=400
        )

    # Valida i dati usando lo schema
    if validate_user_data(req_body):
        return func.HttpResponse(
            json.dumps({"message": "Dati validi"}), 
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            json.dumps({"message": "Dati non validi"}),
            mimetype="application/json",
            status_code=400
        )
