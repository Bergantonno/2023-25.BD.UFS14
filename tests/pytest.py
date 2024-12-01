import pytest
from function_app import analyze_numbers

def test_analyze_numbers():
    # Dati di input
    numbers = [1, 2, 3, 4, 5]

    # Risultati attesi
    expected = {
        "total_sum": 15,
        "mean_value": 3.0,
        "even_count": 2,
        "odd_count": 3,
        "prime_count": 3
    }

    # Confronto con i risultati
    result = analyze_numbers(numbers)
    assert result == expected

def test_empty_list():
    # Test per lista vuota
    numbers = []
    expected = {
        "total_sum": 0,
        "mean_value": 0,
        "even_count": 0,
        "odd_count": 0,
        "prime_count": 0
    }
    assert analyze_numbers(numbers) == expected
