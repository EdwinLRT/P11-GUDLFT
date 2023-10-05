import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

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
    placesRequired = int(request.form['places'])

    # Calcul du nouveau nombre de places et de points
    new_competition_places = int(competition['numberOfPlaces']) - placesRequired
    new_club_points = int(club['points']) - placesRequired

    error_messages = []

    # Vérification si le club a suffisamment de points
    if new_club_points < 0:
        error_messages.append("You don't have enough points to book the seats requested")

    # Vérification si la compétition a suffisamment de places
    if new_competition_places < 0:
        error_messages.append(
            f"There are only {competition['numberOfPlaces']} places available for this competition. You cannot book {placesRequired} places.")

    if not error_messages:
        # Si tout est correct, effectuez la mise à jour
        club['points'] = new_club_points
        competition['numberOfPlaces'] = new_competition_places
        flash('Great-booking complete!')
    else:
        # Si des erreurs se produisent, affichez-les
        for error in error_messages:
            flash(error)
        return render_template('booking.html', club=club, competition=competition)

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))