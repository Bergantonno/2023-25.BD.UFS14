from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

# Endpoint per servire la pagina HTML
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint API per processare i numeri
@app.route("/processa", methods=["POST"])
def processa():
    dati = request.get_json()
    numeri = dati.get("numeri", [])

    try:
        # Converti i numeri in interi
        numeri = list(map(int, numeri))
    except ValueError:
        return jsonify({"errore": "L'input deve contenere solo numeri interi."}), 400

    # Analisi dei numeri
    pari = [n for n in numeri if n % 2 == 0]
    dispari = [n for n in numeri if n % 2 != 0]
    primi = [n for n in numeri if is_prime(n)]

    return jsonify({
        "numeri_pari": pari,
        "numeri_dispari": dispari,
        "numeri_primi": primi
    })

# Funzione per verificare se un numero è primo
def is_prime(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

if __name__ == "__main__":
    app.run(debug=True)
