import azure.functions as func

# Funzione di Azure per gestire richieste HTTP
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Gestisce la richiesta GET per restituire la pagina HTML
    if req.method == "GET":
        html_content = """
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Analisi dei Numeri</title>
            <script>
                async function inviaNumeri() {
                    const input = document.getElementById("numeriInput").value;
                    const numeri = input.split(",").map(num => num.trim());
                    const risultatoDiv = document.getElementById("risultato");

                    try {
                        const response = await fetch("/api/Number-App", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ numeri })
                        });

                        if (!response.ok) {
                            throw new Error("Errore nell'elaborazione dei dati.");
                        }

                        const risultato = await response.json();
                        risultatoDiv.textContent = JSON.stringify(risultato, null, 2);
                    } catch (err) {
                        risultatoDiv.textContent = `Errore: ${err.message}`;
                    }
                }
            </script>
        </head>
        <body>
            <h1>Analisi dei Numeri</h1>
            <p>Inserisci una lista di numeri separati da virgola:</p>
            <input id="numeriInput" type="text" placeholder="Esempio: 2, 3, 4, 5">
            <button onclick="inviaNumeri()">Invia</button>
            <pre id="risultato"></pre>
        </body>
        </html>
        """
        return func.HttpResponse(html_content, mimetype="text/html")

    # Gestisce la richiesta POST per elaborare i numeri
    elif req.method == "POST":
        try:
            dati = req.get_json()
            numeri = dati.get("numeri", [])

            # Converti in numeri interi
            numeri = list(map(int, numeri))

            # Analisi dei numeri
            pari = [n for n in numeri if n % 2 == 0]
            dispari = [n for n in numeri if n % 2 != 0]
            primi = [n for n in numeri if is_prime(n)]

            return func.HttpResponse(
                body=json.dumps({
                    "numeri_pari": pari,
                    "numeri_dispari": dispari,
                    "numeri_primi": primi
                }),
                mimetype="application/json"
            )
        except (ValueError, KeyError):
            return func.HttpResponse(
                body=json.dumps({"errore": "Input non valido. Assicurati di fornire solo numeri interi."}),
                mimetype="application/json",
                status_code=400
            )

# Funzione helper per verificare se un numero è primo
def is_prime(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True
