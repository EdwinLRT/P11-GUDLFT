# !/usr/bin/env python
from pathlib import Path
import pytest
import os
import json
import server


def set_test_mode():
    os.environ['TEST_MODE'] = '1'


set_test_mode()


def check_test_mode():
    if os.environ.get('TEST_MODE'):
        print("Running in TEST_MODE")
    else:
        print("TEST_MODE not activated")


def load_test_data(filepath, key):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data[key]


@pytest.fixture
def mock_data(mocker):
    tests_unit_dir = Path(__file__).parent

    # load test data
    competitions_data = load_test_data(tests_unit_dir / 'config_test_competitions.json', 'competitions')
    clubs_data = load_test_data(tests_unit_dir / 'config_test_clubs.json', 'clubs')

    mocker.patch.object(server, "project_dir", tests_unit_dir)
    mocker.patch.object(server, "clubs", clubs_data)
    mocker.patch.object(server, "competitions", competitions_data)

    # Return mock data for further use in test if needed
    return competitions_data, clubs_data

@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_clubs_page(client):
    response = client.get('/clubs')
    assert response.status_code == 200
    assert b"Clubs" in response.data


def test_valid_email():
    with server.app.test_client() as client:
        response = client.post('/showSummary', data={"email": "cluba@email.com"}, follow_redirects=True)

        assert b"Welcome" in response.data  # checking that the response contains welcome


def test_invalid_email():
    with server.app.test_client() as client:
        response = client.post('/showSummary', data={"email": "invalid@email.com"}, follow_redirects=True)

        assert b"E-mail not found" in response.data  # checking that the flash response contains the error message


def test_purchase_places_page(client, mock_data):
    os.environ['TEST_MODE'] = '1'

    club = "Club A"
    competition = "Competition A"
    points = 1

    response = client.post("/purchasePlaces", data={
        "club": club,
        "competition": competition,
        "places": points})
    data = response.data.decode()
    print(data)
    assert response.status_code == 200
    assert response.status_code == 200
    assert "<li>Great-booking complete ! </li>" in data


def test_booking_more_places_than_points(client, mock_data):

    # Data to use in the test
    competitions_data, clubs_data = mock_data
    club_name = "Club B"
    club_points = [club['points'] for club in clubs_data if club['name'] == club_name][0]
    competition_name = "Competition A"
    # Trying to book more places than the club has points
    places_to_book = club_points + 5

    # Sending the request
    response = client.post("/purchasePlaces", data={
        "club": club_name,
        "competition": competition_name,
        "places": str(places_to_book)  # Convert to string since it's from a form
    })
    data = response.data.decode()
    print(data)

    # Assertions
    assert response.status_code == 200
    assert "You dont have enough points to book the seats requested" in data


def test_booking_more_places_than_competition_places(client, mock_data):


    # Data to use in the test
    competitions_data, clubs_data = mock_data
    club_name = "Club A"
    club_points = [club['points'] for club in clubs_data if club['name'] == club_name][0]
    competition_name = "Competition B"
    # Trying to book more places than the club has points
    places_to_book = club_points

    # Sending the request
    response = client.post("/purchasePlaces", data={
        "club": club_name,
        "competition": competition_name,
        "places": str(places_to_book)  # Convert to string since it's from a form
    })
    data = response.data.decode()
    print(data)

    # Assertions
    assert response.status_code == 200
    assert "You cant book more places than there are available in the competition" in data


def test_deduction_of_points_on_reservation(client, mock_data):
    # Data to use in the test
    competitions_data, clubs_data = mock_data
    club_name = "Club A"
    initial_club_points = [club['points'] for club in clubs_data if club['name'] == club_name][0]
    competition_name = "Competition A"

    # Define the number of places to book
    places_to_book = 8

    # Sending the request to book places
    client.post("/purchasePlaces", data={
        "club": club_name,
        "competition": competition_name,
        "places": str(places_to_book)
    })

    # Get the updated club data
    updated_club_points = [club['points'] for club in server.clubs if club['name'] == club_name][0]

    # Assertions
    assert initial_club_points - places_to_book == updated_club_points


def test_club_points_decrement_on_reservation(client, mock_data):

    # Data to use in the test
    competitions_data, clubs_data = mock_data
    club_name = "Club D"
    initial_club_points = [club['points'] for club in clubs_data if club['name'] == club_name][0]
    competition_name = "Competition C"

    # Define the number of places to book
    placesRequired = 3

    # Sending the request to book places
    client.post("/purchasePlaces", data={
        "club": club_name,
        "competition": competition_name,
        "places": str(placesRequired)
    })

    # Get the updated club points directly from the server's clubs list
    new_club_points = [club['points'] for club in server.clubs if club['name'] == club_name][0]

    # Assertions
    assert new_club_points == initial_club_points - placesRequired


def test_cant_book_passed_events(client, mock_data):

    # Data to use in the test
    competitions_data, clubs_data = mock_data
    club_name = "Club B"
    club_points = [club['points'] for club in clubs_data if club['name'] == club_name][0]
    competition_name = "Competition D"
    # Trying to book places in a passed event
    places_to_book = 1

    # Sending the request
    response = client.post("/purchasePlaces", data={
        "club": club_name,
        "competition": competition_name,
        "places": str(places_to_book)  # Convert to string since it's from a form
    })
    data = response.data.decode()
    print(data)

    # Assertions
    assert response.status_code == 200
    assert "<li>Sorry, you can&#39;t book a past event.</li>" in data


del os.environ['TEST_MODE']
