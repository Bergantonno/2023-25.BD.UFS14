from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
from flask_cors import CORS

# App Flask
app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le origini

# Schema JSON per validare l'input
schema_input = {
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

def is_primo(numero):
    if numero < 2:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

@app.route('/processa', methods=['POST'])
def processa_numeri():
    try:
        # Recupera e valida i dati ricevuti
        dati = request.get_json()
        validate(instance=dati, schema=schema_input)
        
        numeri = dati["numeri"]
        totale = sum(numeri)
        media = totale / len(numeri)
        pari = len([n for n in numeri if n % 2 == 0])
        dispari = len(numeri) - pari
        numeri_primi = [n for n in numeri if is_primo(n)]
        
        # Restituisce il risultato
        return jsonify({
            "totale": totale,
            "media": media,
            "numeri_pari": pari,
            "numeri_dispari": dispari,
            "numeri_primi": numeri_primi
        })
    
    except ValidationError as e:
        return jsonify({"errore": f"Input non valido: {e.message}"}), 400
    except Exception as e:
        return jsonify({"errore": f"Si è verificato un errore: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
