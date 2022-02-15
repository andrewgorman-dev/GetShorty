from flask_shorty import db

# Database Model
class Shorties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(256))
    long = db.Column('long', db.String(256))
    short = db.Column('short', db.String(7), unique=True)
    expiry_time = db.Column('expiry_time', db.DateTime)
    created_at = db.Column('created_at', db.DateTime)

    def __init__(self, name, long, short, expiry_time, created_at):
        self.name = name
        self.long = long
        self.short = short
        self.expiry_time = expiry_time
        self.created_at = created_at