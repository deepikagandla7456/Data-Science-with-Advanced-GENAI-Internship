import pytest

from app import app, analyze_text, validate_name


def test_analyze_text_metrics():
    data = analyze_text("Anna Lee 123")
    assert data["uppercase"] == "ANNA LEE 123"
    assert data["is_palindrome"] is False
    assert data["vowels"] == 4
    assert data["consonants"] >= 3
    assert data["digits"] == 3
    assert data["words"] == 3
    assert data["unique_characters"] >= 6
    assert data["strength_score"] <= 100


def test_validate_name_rules():
    cleaned, error = validate_name("  Alice ")
    assert cleaned == "Alice"
    assert error is None

    cleaned, error = validate_name("".ljust(81, "a"))
    assert cleaned is None
    assert "too long" in error

    cleaned, error = validate_name("")
    assert cleaned is None
    assert error is not None


def test_api_response(client):
    resp = client.get("/api/analyze", query_string={"user": "Bob"})
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["uppercase"] == "BOB"

    bad_resp = client.get("/api/analyze", query_string={"user": ""})
    assert bad_resp.status_code == 400


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as client:
        yield client
