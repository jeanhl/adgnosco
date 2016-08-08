"""Models and database functions for access monitoring project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Entrance(db.Model):
    """Individual entrances of a building."""

    __tablename__ = "entrance"

    entrance_id = db.Column(db.Integer, primary_key=True)
    entrance_name = db.Column(db.String(20), nullable=False)
    building_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Entr_id:%d  Entr_name:%s  Bld_id:%s  >" % (self.entrance_id, 
                                                             self.entrance_name,
                                                             self.building_id)
    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("user", order_by=somethingsomething))

    class Building(db.Model):
    """Individual Buildings in a campus."""

    __tablename__ = "building"

    building_id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(20), nullable=False)
    building_address = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Entr_id:%d  Entr_name:%s  Bld_id:%s  >" % (self.entrance_id, 
                                                             self.entrance_name,
                                                             self.building_id)
    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("user", order_by=somethingsomething))


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
