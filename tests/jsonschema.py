import jsonschema
from function_app import analyze_numbers

# Definizione dello schema JSON
schema = {
    "type": "object",
    "properties": {
        "total_sum": {"type": "integer"},
        "mean_value": {"type": "number"},
        "even_count": {"type": "integer"},
        "odd_count": {"type": "integer"},
        "prime_count": {"type": "integer"}
    },
    "required": ["total_sum", "mean_value", "even_count", "odd_count", "prime_count"]
}

def test_jsonschema_validation():
    numbers = [1, 2, 3, 4, 5]
    result = analyze_numbers(numbers)
    
    # Validazione dello schema
    jsonschema.validate(instance=result, schema=schema)
