"""Utility file to seed access database from seed data in seed_data/"""

from model import Entrance, Building, Personnel, Entries, connect_to_db, db
from server import app
from sqlalchemy import func


def load_entrance():
    """Load entryways from entryway into database."""

    print "Entrance"

    for i, row in enumerate(open("seed_data/entryway.csv")):
        row = row.rstrip()
        entrance_id, entrance_name, building_id = row.split(",")

        entrance = Entrance(entrance_id=entrance_id,
                            entrance_name=entrance_name,
                            building_id=building_id)

        #adding to the session
        db.session.add(entrance)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    #commiting the changes to update the database
    db.session.commit()


def load_building():
    """Load buildings from building into database."""

    print "Buildings"

    for i, row in enumerate(open("seed_data/building.csv")):
        row = row.rstrip()
        building_id, building_name, building_address = row.split(",")

        building = Building(building_id=building_id,
                            building_name=building_name,
                            building_address=building_address)

        #adding to the session
        db.session.add(building)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    #commiting the changes to update the database
    db.session.commit()


def load_personnel():
    """Load personnel from people into database."""

    print "Personnel"

    for i, row in enumerate(open("seed_data/people.csv")):
        row = row.rstrip()
        person_id, person_name, keycode, manager = row.split(",")

        print person_name

        person = Personnel(person_id=person_id,
                           person_name=person_name,
                           keycode=keycode,
                           manager=manager)

        #adding to the session
        db.session.add(person)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    #commiting the changes to update the database
    db.session.commit()


def load_entries():
    """Load entries from entries into database."""

    print "Entries"

    for i, row in enumerate(open("seed_data/entries.csv")):
        row = row.rstrip()
        id, person_id, entrance_id, building_id, datentime = row.split(",")

        entry = Entries(id=id,
                        person_id=person_id,
                        entrance_id=entrance_id,
                        building_id=building_id,
                        datentime=datentime)

        #adding to the session
        db.session.add(entry)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    #commiting the changes to update the database
    db.session.commit()


def set_val_entry_id():
    """Set value for the next entry id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Entries.id)).one()
    max_id = int(result[0])

    # Set the value for the next entries_id to be max_id + 1
    query = "SELECT setval('entries_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_building()
    load_personnel()
    load_entrance()    
    load_entries()
    set_val_entry_id()
