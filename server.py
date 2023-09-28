import json
import os   # to get the environment variable TEST_MODE
from flask import Flask, render_template, request, redirect, flash, url_for
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'something_special'
project_dir = Path(__file__).parent
def loadClubs():
    if os.environ.get('TEST_MODE'):
        data_path = 'tests/config_test_clubs.json'
    else:
        data_path = 'clubs.json'
    with open(data_path) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def loadCompetitions():
    if os.environ.get('TEST_MODE'):
        data_path = 'tests/config_test_competitions.json'
    else:
        data_path = 'competitions.json'
    with open(data_path) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions



competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
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

    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    print("Request form club:", request.form['club'])
    print("Clubs:", clubs)
    placesRequired = int(request.form['places'])

    print(f"trying to book {placesRequired} places")

    # Calculate the new number of places and points
    new_competition_places = int(competition['numberOfPlaces']) - placesRequired
    new_club_points = int(club['points']) - placesRequired
    print(f"new competition places: {new_competition_places}")
    print(f"new club points: {new_club_points}")

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
        flash('Great-booking complete!')
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