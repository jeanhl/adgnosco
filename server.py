"""Adgnosco Server"""

import arrow
from collections import defaultdict
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func
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

def set_val_entry_id():
    """Set value for the next entry id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Entries.id)).one()
    max_id = int(result[0])

    return max_id


@app.route('/keyless', methods=['POST'])
def keyless_entry():
    """Processes the keyless entry."""
    person_id = session['user_id']
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

    datetime_now = arrow.now('US/Pacific').datetime
    print arrow.now('US/Pacific').datetime

    max_id = set_val_entry_id()
    query = "SELECT setval('entries_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()
    # entring new entry into the database
    new_entry = Entries(entrance_id=entrance_id,
                        person_id=person_id,
                        building_id=building_id,
                        datentime=datetime_now)

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
    person_id = session['user_id']

    entries = Entries.query.filter_by(person_id=person_id).all()


    return render_template('entries.html', entries=entries)


@app.route('/monthly.json')
def monthly_logs_data():
    """Return data about entries on a monthly basis"""
    # You will want to make this a get request in the future
    # pass in the month so that you'll get the report for THAT month
    person_id = session['user_id']

    ##### month = request.args.get('month')
    month = 8
    entries = Entries.query.all()

    # making nested dictionaries of the entries by door by day for the month specified
    # dict_of_doors  = {entrance_id1:{day1:count1, day2:count2},
    #                    entrance_id2:{day3:count3, day4:count4}
    #                   }
    dict_of_entries = {}
    doors = Entrance.query.all()
    for door in doors:
        entriess = Entries.query.filter(Entries.entrance_id == door.entrance_id).all()
        inner_dict = defaultdict(int)
        for entry in entriess:
            if entry.datentime.date().month == month:
                day_of_month = entry.datentime.date().day
                inner_dict[day_of_month] += 1
        dict_of_entries[door.entrance_id] = inner_dict

    list_color = ['#0001ff', '#59fa67', '#fff138',
                  '#e62600', '#dd3cc4', '#b7cb34',
                  '#ff6600', '#22dc09', '#af040c']

    # largest structure, the value is a list of dictionaries
    monthly_dict = {'datasets': []}


    # middle structure, making the large list of dictionaries
    buildings = Building.query.all()
    count = 0
    for building in buildings:
        building_name = building.building_name
        med_dict = {'label': building_name } 
        med_dict['data']=[]
        med_dict['backgroundColor'] = list_color[count]
        med_dict['hoverBackgoundColor'] = list_color[count]
        monthly_dict['datasets'].append( med_dict )
        count += 1

        # smallest structure, making the list of mini dictionaries
        for entry in entries:
            if entry.building_id == building.building_id:
                x_value = entry.datentime.date().day
                y_value = entry.entrance_id
                # getting the r_value from the dict_of_entries above
                days = dict_of_entries.get(y_value)
                r_value = days.get(x_value) * 5
                # back to making the mini dictionary
                mini_dict = {'x':x_value, 'y':y_value, 'r':r_value}
                med_dict['data'].append(mini_dict)

    return jsonify(monthly_dict)


@app.route('/building.json')
def building_logs_data():
    """Return data about entries into a building on a monthly basis"""
    # You will want to make this a get request in the future
    # pass in the month so that you'll get the report for THAT month
    person_id = session['user_id']

    month = 8
    building_id = 1
    ##### month = request.args.get('month')

    # making nested dictionaries of the entries by door by day for the month specified
    # dict_of_doors  = {entrance_id1:{day1:{hour1a:count1b, hour1b:count1b}, day2:{hour2a:count2b, hour2b:count2b}},
    #                   entrance_id2:{day1:{hour1a:count1b, hour1b:count1b}, day2:{hour2a:count2b, hour2b:count2b}}
    #                   }
    dict_of_entries = {}
    byday_dict = {}
    byhour_dict = defaultdict(int)
    # hirarchy: dict_of_entries > entrace_dict > byday_dict > byhour_dict

    # filtering all entries by the month and building specified
    entriesbybuilding = (Entries.query.filter(Entries.building_id==building_id).all())
    for entrybybuilding in entriesbybuilding:
        if entrybybuilding.datentime.date().month==month:
            for eachday in range(31):
                if entrybybuilding.datentime.date().day == eachday:
                    # making a dictionary with count of entries
                    hourly = entrybybuilding.datentime.time().hour
                    byhour_dict[hourly] += 1
                byday_dict[entrybybuilding.datentime.date().day] = byhour_dict
            dict_of_entries[entrybybuilding.entrance_id] = byday_dict

    print dict_of_entries

    list_color = ['#0001ff', '#59fa67', '#fff138',
                  '#e62600', '#dd3cc4', '#b7cb34',
                  '#0001ff', '#59fa67', '#fff138',
                  '#e62600', '#dd3cc4', '#b7cb34',
                  '#0001ff', '#59fa67', '#fff138',
                  '#e62600', '#dd3cc4', '#b7cb34',
                  '#0001ff', '#59fa67', '#fff138',
                  '#e62600', '#dd3cc4', '#b7cb34',
                  '#ff6600', '#22dc09', '#af040c']

    # largest structure, the value is a list of dictionaries
    building_dict = {'datasets': []}

    entries = Entries.query.all()

    # middle structure, making the large list of dictionaries
    count = 0
    for entry2 in entriesbybuilding:
        entranceid = entry2.id
        med_dict = {'label': entranceid}
        med_dict['data']=[]
        med_dict['backgroundColor'] = list_color[count]
        med_dict['hoverBackgoundColor'] = list_color[count]
        building_dict['datasets'].append( med_dict )
        count += 1

        # smallest structure, making the list of mini dictionaries
        building = Building.query.filter(Building.building_name == "Main").first()
        if entry2.building_id == building.building_id:
            x_value = entry2.datentime.date().day
            y_value = entry2.datentime.time().hour
            # getting the r_value from the dict_of_entries above
            dailylog = dict_of_entries.get(entranceid)
            print dailylog
            hourlylog = dailylog.get(x_value)
            r_value = hourlylog.get(y_value)
            # back to making the mini dictionary
            mini_dict = {'x':x_value, 'y':y_value, 'r':r_value}
            med_dict['data'].append(mini_dict)
    
    return jsonify(building_dict)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)
