# """CRUD operations."""

from datetime import datetime, timedelta
from model import db, User, Complex, Description, Inventory
import os

# Twilio config
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = '+12029461857'
client = Client(account_sid, auth_token)

def lookup_mobile_number(mobile):
    try:
        lookup = client.lookups.phone_numbers(mobile).fetch(type=['carrier'])
        return lookup.phone_number
    except Exception as e:
        return None


def create_user(email, password, fname, lname, complex_id, mobile_number):
    """Create and return a new user."""

    user = User(email=email.strip(), 
                password=password,
                fname=fname.strip(), 
                lname=lname.strip(),
                complex_id=complex_id,
                mobile_number=mobile_number)
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


def get_completed_listings(complex_id):
    """Return all completed herb requests for a given complex"""

    return Inventory.query.filter(Inventory.status == 4, Inventory.complex_id == complex_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email.lower()).first()


def get_user_by_mobile(mobile):
    """Return a user by mobile number e.164 format"""

    return User.query.filter(User.mobile_number == mobile).first()


def get_user_by_id(user_id):
    """Return a user by id"""

    return User.query.filter(User.user_id == user_id).first()


def get_herb_by_inventory_id(inventory_id):
    """Get singular herb from inventory """

    return Inventory.query.filter_by(inventory_id=inventory_id).one()


def send_notification(to_number, msg):

    try:
        message = client.messages \
            .create(
                 body=msg,
                 from_=twilio_number,
                 to=to_number
             )
    except Exception as error:
        # LATER TODO: maybe send out email if twilio fails?

        print(f'Something is wrong with your Twilio credentials: {error}')
        return True

    return True


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
