import azure.functions as func
import json
import logging

app = func.FunctionApp()

# Funzione per calcolare i dettagli sui numeri

def analyze_numbers(numbers):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    total_sum = sum(numbers)
    mean_value = total_sum / len(numbers) if numbers else 0
    even_count = len([num for num in numbers if num % 2 == 0])
    odd_count = len(numbers) - even_count
    prime_count = len([num for num in numbers if is_prime(num)])

    return {
        "total_sum": total_sum,
        "mean_value": mean_value,
        "even_count": even_count,
        "odd_count": odd_count,
        "prime_count": prime_count,
    }

# Generare la pagina HTML del form

def generate_html_form():
    return """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Analizzatore di Numeri</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #e3f2fd;
                color: #1a237e;
                text-align: center;
                padding: 20px;
            }
            .container {
                background: #bbdefb;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                display: inline-block;
                text-align: center;
            }
            h1 {
                color: #0d47a1;
            }
            form {
                margin-top: 20px;
            }
            input, button {
                padding: 10px;
                margin: 10px 0;
                width: 90%;
                border: 1px solid #90caf9;
                border-radius: 5px;
            }
            button {
                background-color: #1976d2;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #1565c0;
            }
        </style>
    </head>
    <body>
        <h1>Benvenuto nell'Analizzatore di Numeri</h1>
        <div class="container">
            <p>Inserisci una lista di numeri separati da virgola:</p>
            <form action="/api/Number-App" method="post">
                <input type="text" name="numbers" placeholder="Es: 2,3,5,8,11" required>
                <button type="submit">Analizza</button>
            </form>
        </div>
    </body>
    </html>
    """

# Generare la pagina HTML con i risultati

def generate_html_result(response_data):
    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Risultati Analizzatore di Numeri</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #e3f2fd;
                color: #1a237e;
                text-align: center;
                padding: 20px;
            }}
            .container {{
                background: #bbdefb;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                display: inline-block;
                text-align: left;
            }}
            h1 {{
                color: #0d47a1;
            }}
            .result {{
                margin-bottom: 15px;
                font-size: 1.1rem;
            }}
        </style>
    </head>
    <body>
        <h1>Risultati dell'Analizzatore di Numeri</h1>
        <div class="container">
            <p class="result">Somma totale: <strong>{response_data['total_sum']}</strong></p>
            <p class="result">Media: <strong>{response_data['mean_value']}</strong></p>
            <p class="result">Numeri pari: <strong>{response_data['even_count']}</strong></p>
            <p class="result">Numeri dispari: <strong>{response_data['odd_count']}</strong></p>
            <p class="result">Numeri primi: <strong>{response_data['prime_count']}</strong></p>
        </div>
    </body>
    </html>
    """

@app.route(route="Number-App", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST"])
def number_app(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    if req.method == "GET":
        return func.HttpResponse(generate_html_form(), mimetype="text/html", status_code=200)

    # Gestisci il POST
    numbers_str = req.form.get("numbers")

    if numbers_str:
        try:
            # Convertire i numeri da stringa a lista di interi
            numbers = [int(n) for n in numbers_str.split(",")]
            results = analyze_numbers(numbers)
            return func.HttpResponse(generate_html_result(results), mimetype="text/html", status_code=200)
        except ValueError:
            return func.HttpResponse("Errore: Assicurati di inserire solo numeri separati da virgola.", mimetype="text/html", status_code=400)
    else:
        return func.HttpResponse("Errore: Il campo numeri è richiesto.", mimetype="text/html", status_code=400)
