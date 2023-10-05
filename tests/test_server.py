import pytest
from server import app, loadClubs


app.config['TESTING'] = True

# Fake datas used for testing purposes
test_clubs = [
    {"name": "Club A", "email": "cluba@email.com"},
    {"name": "Club B", "email": "clubb@email.com"}
]

def test_valid_email():
    with app.test_client() as client:
        response = client.post('/showSummary', data={"email": "cluba@email.com"}, follow_redirects=True)

        assert b"Welcome" in response.data # checking that the response contains welcome

def test_invalid_email():
    with app.test_client() as client:
        response = client.post('/showSummary', data={"email": "invalid@email.com"}, follow_redirects=True)

        assert b"E-mail not found" in response.data # checking that the flash response contains the error message

