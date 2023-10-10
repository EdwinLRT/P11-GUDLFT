import json
import os  # to get the environment variable TEST_MODE
from flask import Flask, render_template, request, redirect, flash, url_for
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'something_special'
project_dir = Path(__file__).parent


def loadClubs():
    if os.environ.get('TEST_MODE'):
        data_path = 'tests/unit/config_test_clubs.json'
    else:
        data_path = 'clubs.json'
    with open(data_path) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    if os.environ.get('TEST_MODE'):
        data_path = 'tests/unit/config_test_competitions.json'
    else:
        data_path = 'competitions.json'
    with open(data_path) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


competitions = loadCompetitions()
print(competitions)
clubs = loadClubs()
print(clubs)


def update_club_data(clubs):
    if os.environ.get('TEST_MODE'):
        data_path = 'tests/unit/config_test_clubs.json'
    else:
        data_path = 'clubs.json'
    with open(data_path, 'w') as f:
        json.dump({"clubs": clubs}, f, indent=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Bring the user to the welcome page after login and display the summary.
    Also check if the user email is in the list.
    """
    club = [club for club in clubs if club['email'] == request.form['email']]
    if not club:
        flash('E-mail not found. Please try again.')
        return redirect(url_for('index'))
    club = club[0]

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        # Check if the competition datetime - if it is in the past, don't allow booking
        competition_date = datetime.fromisoformat(foundCompetition['date'])
        if competition_date < datetime.now():
            flash("Sorry, you can't book a past event.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Check if the competition datetime - if it is in the past, don't allow booking
    competition_date = datetime.fromisoformat(competition['date'])
    if competition_date < datetime.now():
        flash("Sorry, you can't book a past event.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Check the number of places available for reservation
    # Obtain the number of places already reserved for this competition
    current_booked = club.get('competitions_booked', {}).get(competition['name'], 0)
    total_booked = current_booked + placesRequired

    if total_booked > 12:
        flash(f"You can't book more than 12 places for {competition['name']}.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Calculate the new number of places and points
    new_competition_places = int(competition['numberOfPlaces']) - placesRequired
    new_club_points = int(club['points']) - placesRequired
    print(f"new competition places: {new_competition_places}")
    print(f"new club points: {new_club_points}")

    # Update of the total number of places reserved by the club for this competition
    club.setdefault('competitions_booked', {})[competition['name']] = total_booked

    # Save updated data in JSON files
    if os.environ.get('TEST_MODE'):
        print("TEST MODE - not saving data to JSON files")
    else:
        print("Saving data to JSON files")
        update_club_data(clubs)

    error_messages = []

    # Check if the club has enough points
    if new_club_points < 0:
        error_messages.append("You dont have enough points to book the seats requested")
        print("You dont have enough points to book the seats requested")

    # Check if there are enough places available in the competition
    if new_competition_places < 0:
        error_messages.append(
            "You cant book more places than there are available in the competition"
            f"There are only {competition['numberOfPlaces']} places available for this competition. You cannot book {placesRequired} places.")

    if not error_messages:
        # if no errors, update the number of places and points
        club['points'] = new_club_points
        competition['numberOfPlaces'] = new_competition_places
        flash("Great-booking complete ! ")
        # flash(f'you have booked {placesRequired} places for {competition["name"]}')
        print("Great-booking complete!")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        # If errors are found, display them and return to the booking page
        for error in error_messages:
            flash(error)
        return render_template('welcome.html', club=club, competitions=competitions,
                               error_messages=error_messages)

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubs', methods=['GET'])
def showClubs():
    return render_template('clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
