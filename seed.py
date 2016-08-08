"""Utility file to seed access database from seed data in seed_data/"""

from model import Entrance, Building, Personnel, Entries, connect_to_db, db
from server import app


def load_entrance():
    """Load entryways from entryway into database."""

    print "Entrance"

    for i, row in enumerate(open("seed_data/entryway")):
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

    for i, row in enumerate(open("seed_data/building")):
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

    for i, row in enumerate(open("seed_data/people")):
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

    for i, row in enumerate(open("seed_data/entries")):
        row = row.rstrip()
        id, person_id, entrance_id, datentime = row.split(",")

        entry = Entries(id=id,
                        person_id=person_id,
                        entrance_id=entrance_id,
                        datentime=datentime)

        #adding to the session
        db.session.add(entry)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    #commiting the changes to update the database
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
