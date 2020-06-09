"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Complex(db.Model):
    """A movie rating."""

    __tablename__ = 'complexes'

    complex_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    complex_name = db.Column(db.String(50))
    complex_address = db.Column(db.String(75))
    status = db.Column(db.Integer)

    #user = db.relationship('User', backref='apartments')

    def __repr__(self):
        return f'<Complex complex_id={self.complex_id} apt_name={self.complex_name}>'   



class User(db.Model):
    """A User"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.Text, nullable=True)
    complex_id = db.Column(db.Integer, db.ForeignKey('complexes.complex_id'), nullable=False)

    # Backrefs
    complexes = db.relationship('Complex')
    inventories = db.relationship('Inventory')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'




class Description(db.Model):
    """A movie rating."""

    __tablename__ = 'descriptions'

    herb_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    herb_name = db.Column(db.String(15), unique=True, nullable=False)
    descript = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=False, default='default.png')


    def __repr__(self):
        return f'<Herb_Description herb_id={self.herb_id} herb_name={self.herb_name}>'   

class Inventory(db.Model):
    """An Herb Inventory."""

    __tablename__ = 'inventories'

    inventory_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    pickup_user_id = db.Column(db.Integer, unique=True, nullable=True)
    listing_date = db.Column(db.DateTime, nullable=False)
    # Status: 0=incative/delisted, 1=active/listed, 2=pending pickup, 3=completed/ picked up
    status = db.Column(db.Integer, nullable=False)
    pickup_instructions = db.Column(db.String(200), nullable=True)
    last_update = db.Column(db.DateTime, nullable=True)
    herb_id = db.Column(db.Integer, db.ForeignKey('descriptions.herb_id'), nullable=False)
    herb_qty = db.Column(db.Integer, nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    user_img_url = db.Column(db.String, nullable=True)
    complex_id = db.Column(db.Integer, db.ForeignKey('complexes.complex_id'), nullable=False)
 
    #the inventory backref is to the description. 
    herb = db.relationship('Description')

    def __repr__(self):
        return f'<Herb Inventory inventory_id={self.inventory_id} herb_id={self.herb_id}>'        



class Messaging(db.Model):
    """A movie rating."""

    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.inventory_id'), nullable=False)
    msg_content = db.Column(db.String(100), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)


    #users = db.relationship('User', backref='messages')


    def __repr__(self):
        return f'<Messaging message_id={self.message_id} inventory_id={self.inventory_id}>'   




def connect_to_db(flask_app, db_uri='postgresql:///herbmates', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
