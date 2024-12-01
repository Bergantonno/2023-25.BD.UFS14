from function_app import generate_html_form, generate_html_result

def test_generate_html_form(snapshot):
    # Test per il form HTML
    form_html = generate_html_form()
    snapshot.assert_match(form_html, "html_form_snapshot.html")

def test_generate_html_result(snapshot):
    # Test per il risultato HTML
    result_data = {
        "total_sum": 15,
        "mean_value": 3.0,
        "even_count": 2,
        "odd_count": 3,
        "prime_count": 3
    }
    result_html = generate_html_result(result_data)
    snapshot.assert_match(result_html, "html_result_snapshot.html")
