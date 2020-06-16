# """CRUD operations."""

from datetime import datetime, timedelta
from model import db, User, Complex, Description, Inventory, Messaging


def create_user(email, password, fname, lname, complex_id):
    """Create and return a new user."""

    user = User(email=email, 
                password=password, 
                fname=fname, 
                lname=lname,
                complex_id=complex_id)

    db.session.add(user)
    db.session.commit()

    return user


def add_herbs_to_inventory(herb_id, user_id, listing_date, complex_id, pickup_instructions, herb_qty=1):
    """Add an herbs for a given complex"""

    listing = Inventory(herb_id=herb_id,
                     user_id=user_id,
                     listing_date=listing_date,
                     complex_id=complex_id,
                     herb_qty=herb_qty,
                     exp_date=listing_date + timedelta(days=5),
                     pickup_instructions=pickup_instructions,
                     status=1,
                     )   
    db.session.add(listing)
    db.session.commit()

    return listing


def get_herbs_in_inventory(complex_id, user_id):
    """Return all active herbs for a given complex"""

    return Inventory.query.filter((Inventory.status==1) | (Inventory.status==2) | (Inventory.status==3))\
    .filter(Inventory.complex_id==complex_id)\
    .filter((Inventory.user_id==user_id) | (Inventory.pickup_user_id==user_id) | (Inventory.pickup_user_id==None))\
    .filter(Inventory.exp_date >= datetime.now())\
    .order_by(Inventory.status.desc())

    #multiple users works?


def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email.lower()).first()

def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).first()

def get_herb_by_inventory_id(inventory_id):
    """ Get singular inventory """
    return Inventory.query.filter_by(inventory_id=inventory_id).one()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
