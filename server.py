"""Adgnosco Server"""

import arrow
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Entrance, Building, Personnel, Entries, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    # checking to see if user is in database
    user = Personnel.query.filter_by(person_id=username).first()
    print user

    # problems with user not being in database
    if not user:
        flash("No such ID registered.")
        return redirect('/')
    password = int(password)
    if user.keycode != password:
        flash("Password does not match password on record.")
        return redirect('/')

    # user is in database. Log them in and add them to the session
    session["user_id"] = user.person_id

    flash("Logged in successfully")
    return redirect('/profilepage')


@app.route('/profilepage', methods=['GET'])
def profile_page():
    """Shows user profile page."""

    # only shows the profile of whoever is in the session
    person_id = session['user_id']
    user = Personnel.query.filter_by(person_id=person_id).first()


    # Have the details of the user. DONE
    # Have a button to go:
        # remote access to a door DONE
        # view their entry logs DONE MAYBE
    # Manager:
        # Be able to view logs DONE MAYBE
        # Be able to register a user DONE
        # Reach: Be able to change key code of a user
        # Reach: Be able to deactivate a user

    return render_template('profilepage.html', user=user)


@app.route('/register', methods=['POST'])
def register_process():
    """Processes a registration form."""

    # gets the information from the register form
    # adds the information to the database with checks

    person_id = request.form['username']
    person_name = request.form['name']
    keycode = request.form['password']
    manager = request.form['manager']

    new_user = Personnel(person_id=person_id,
                         person_name=person_name,
                         keycode=keycode,
                         manager=manager)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/profilepage')


@app.route('/opensesame')
def show_keyless_entry():
    """ Shows the template for keyless entry """

    return render_template('keyless.html')


@app.route('/keyless', methods=['POST'])
def keyless_entry():
    """Processes the keyless entry."""
    person_id = session['user_id']
    print person_id
    user = Personnel.query.filter_by(person_id=person_id).first()

    # gets the info from the keyless entry
    entrance_id = request.form['doorid']
    password = request.form['password']
    password = int(password)

    entrance = Entrance.query.filter_by(entrance_id=entrance_id).first()

    # checks if the entrance_id is in the database
    if not entrance:
        flash("No such door.")
        return redirect('/opensesame')

    # checking keycode for the user logged in
    if user.keycode != password:
        flash("Keycode doesn't match.")
        return redirect('/')

    building_id = entrance.building_id

    timenow = arrow.utcnow().to('US/Pacific')
    timestring = timenow.isoformat()

    # entring new entry into the database
    new_entry = Entries(entrance_id=entrance_id,
                        person_id=person_id,
                        building_id=building_id,
                        datentime=timestring)

    # adding to database
    db.session.add(new_entry)
    db.session.commit()

    # if there was a hardware, this would send an unlocking signal to it
    # successful door unlocking
    flash("Door unlocked. You can now enter.")
    return redirect('/profilepage')


@app.route('/entries')
def show_entries():
    """Shows the entries of the user selected"""

    # Default:
        # shows the entries for the month
    # Manager:
        # Ability to filter by
            # Person
            # Building
            # Entryway

    # Reach: do a visual representation of the entries

    return render_template('entries.html')




    # new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    # db.session.add(new_user)
    # db.session.commit()

    # flash("User %s added." % email)
    # return redirect("/users/%s" % new_user.user_id)



# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)
