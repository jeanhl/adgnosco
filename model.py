"""Models and database functions for access monitoring project."""

"""Need some data to test the Graphql query"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Entrance(db.Model):
    """Individual entrances of a building."""

    __tablename__ = "entrances"

    entrance_id = db.Column(db.Integer, primary_key=True)
    entrance_name = db.Column(db.String(20), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Entr_id:%d  Entr_name:%s  Bld_id:%s  >" % (self.entrance_id,
                                                             self.entrance_name,
                                                             self.building_id)

class Building(db.Model):
    """Individual Buildings in a campus."""

    __tablename__ = "buildings"

    building_id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(20), nullable=False)
    building_address = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Building id: %d  Building name: %s  Building add: %s  >" % (self.building_id,
                                                                              self.building_name,
                                                                              self.building_address)

class Personnel(db.Model):
    """ People who have access to the building. """

    __tablename__ = "personnels"

    person_id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(50), nullable=False)
    keycode = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Person id: %d  Person name: %s   Keycode: %d  Manager: %s >" % (self.person_id,
                                                                                   self.person_name,
                                                                                   self.keycode,
                                                                                   self.manager)
class Entries(db.Model):
    """ Individual entries into a building via an entryway. """

    __tablename__ = "entries"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('personnels.person_id'), nullable=False)
    entrance_id = db.Column(db.Integer, db.ForeignKey('entrances.entrance_id'), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=False)
    datentime = db.Column(db.DateTime(timezone=True), nullable=False)

    # Defining relationships to person, entrance, building
    person = db.relationship("Personnel",
                             backref=db.backref("entry"))
    entrance = db.relationship("Entrance",
                               backref=db.backref("entry"))
    building = db.relationship("Building",
                               backref=db.backref("entry"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Entry id: %d  Person id: %d  Entrance id: %d   Building id: %d   At: %s   >" % (self.id,
                                                                                                  self.person_id,
                                                                                                  self.entrance_id,
                                                                                                  self.building_id,
                                                                                                  self.datentime)

class Recognized(db.Model):
    """ Individual recognized through facial recognition feature. """

    __tablename__ = "recognized"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('personnels.person_id'), nullable=False)
    entrance_id = db.Column(db.Integer, db.ForeignKey('entrances.entrance_id'), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=False)
    datentime = db.Column(db.DateTime(timezone=True), nullable=False)
    conf_lvl = db.Column(db.Float, nullable=True)

    # Defining relationships to person, entrance, building
    person = db.relationship("Personnel",
                             backref=db.backref("recognized"))
    entrance = db.relationship("Entrance",
                               backref=db.backref("recognized"))
    building = db.relationship("Building",
                               backref=db.backref("recognized"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Recognized id: %d  Person id: %d  Entrance id: %d   Building id: %d   At: %s   >" % (self.id,
                                                                                                  self.person_id,
                                                                                                  self.entrance_id,
                                                                                                  self.building_id,
                                                                                                  self.datentime)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///access'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
