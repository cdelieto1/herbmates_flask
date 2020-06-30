"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from datetime import datetime
from model import *
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

STATIC_URL = '/static/'
IMG_ROOT ='%s%s' % (STATIC_URL, 'img/')
#I couldn't get the img token to render for react so had to append this

def check_auth():
    try:
        if session['is_authenticated']:
            return True
        else:
            return False
    except:
        # invoked for a not logged-in user
        return False


@app.route('/')
def homepage():
    """View homepage ONLY IF authenticated."""

    if not check_auth():
        return redirect('/login')

    user = crud.get_user_by_id(session['user_id'])
    if not user:
        return redirect('/logout')

    inventory = crud.get_herbs_in_inventory(user.complex_id, user.user_id)

    inventory_count = inventory.count()
    #inventory variable wouldn't pass a count in templating. BaseQuery error. 
    
    completed_listings = crud.get_completed_listings(user.complex_id)

    return render_template('homepage.html', user=user, inventory_count=inventory_count, inventory=inventory, completed_listings=completed_listings)

@app.route('/react')
def homepage_react():
    """View REACT homepage ONLY IF authenticated."""

    if not check_auth():
        return redirect('/login')
 
    return render_template('homepage_react.html')


@app.route('/get-inventory', methods=['GET'])
def get_inventory():
    """View REACT homepage ONLY IF authenticated."""

    if not check_auth():
        return redirect('/login')
 
    user = crud.get_user_by_id(session['user_id'])
    if not user:
        return redirect('/logout')

    inventory = crud.get_herbs_in_inventory(user.complex_id, user.user_id)

    listings = []
    for listing in inventory:
        listings.append({
            'inventory_id': listing.inventory_id,
            'session_user_id': user.user_id,
            'user_id': listing.user_id,
            'pickup_user_id': listing.pickup_user_id,
            'status': listing.status,
            'fname': listing.user.fname.title(),
            'herb_name': listing.herb.herb_name,
            'herb_qty': listing.herb_qty,
            'exp_date': listing.exp_date.strftime('%A %d, %B %Y'),
            'img_url': '%s%s' % (IMG_ROOT, listing.herb.img_url),
            'pickup_instructions': listing.pickup_instructions})


    #inventory_count = inventory.count()
    #completed_listings = crud.get_completed_listings(user.complex_id)

    return jsonify({'success': True,
                    'data': listings})

@app.route('/signup', methods=['GET', 'POST'])
def register_user():
    """Create a new user."""


    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        complex_id = request.form.get('complex')
        mobile = request.form.get('mobile', type=int)

        if password != confirm_password:
            flash('Passwords do not match. Try again')

        user = crud.get_user_by_email(email)

        if user:
            flash('This email or mobile number has already been registered. Please sign in instead or reset your password!')
        else:
            user = crud.create_user(email, password, fname, lname, complex_id, mobile)
            session['is_authenticated'] = True
            session['user_id'] = user.user_id
            flash('Account created!')
            return redirect('/')

    complexes = Complex.query.all()

    return render_template('login.html', complexes=complexes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to Herbmates"""

    email = request.form.get('email')
    password = request.form.get('password')
    complexes = Complex.query.all()
    #complexes populates the dropdown tab on the login page

    if request.method == 'POST':
        user = crud.get_user_by_email(email) # a query to see if they exist first
        if user and user.password == password:
            #log me in / create session
            session['is_authenticated'] = True
            session['user_id'] = user.user_id
            return redirect('/')
        else:
            flash('Either email or password are incorrect!')

    return render_template('login.html', complexes=complexes)


@app.route('/list')
def add_herbs():
    """Add an herb"""

    if not check_auth():
        return redirect('/login')

    user = crud.get_user_by_id(session['user_id'])
    herbs = Description.query.all()

    return render_template('list_herb.html', user=user, herbs=herbs)

@app.route('/list', methods=['POST'])
def add_to_list():
    """Add an herb"""

    if not check_auth():
        return redirect('/login')

    user = crud.get_user_by_id(session['user_id'])

    herb_id = request.form.get('herb')

    listing_date=datetime.now()

    #TODO: add a qty field into form. For now, we set it to 1 as a forced value.
    herb_qty = request.form.get('herb_qty')
    herb_qty = 1

    pickup_instructions = request.form.get('description')

    listing = crud.add_herbs_to_inventory(herb_id, 
                                         user.user_id,
                                         listing_date,
                                         user.complex_id,
                                         pickup_instructions,
                                         herb_qty)

    if not listing:
        flash('Problem listing herb. Please try again!')

    return redirect('/')

@app.route('/update_inventory_status', methods=['GET', 'POST'])
def update_inventory_status():

    if not check_auth():
        return 'user not authenticated', 403 # forbidden

    user_id = session['user_id'] 
    task = request.form.get('task', type=str) # pickup, ready, complete, delete
    inventory_id = request.form.get('inventory_id', type=int)
    pickup_instructions = request.form.get('pickup_instructions', type=str) 

    #lookup singular herb in inventory
    inventory = crud.get_herb_by_inventory_id(inventory_id)

    if inventory:

        if task == 'pickup' and inventory.status == 1 and inventory.user_id != user_id: # can't book my own herb. 
            inventory.pickup_user_id = user_id
            inventory.status = 2
            
            crud.send_notification(inventory.user.mobile_number, f'{inventory.pickup_user.fname.strip().title()} requested a pickup for {inventory.herb.herb_name}')

        elif task == 'ready' and inventory.status == 2 and inventory.user_id == user_id: # only person who posted it can update pickup instructions and make it available

            #pickup_instructions = request.form.get('pickup_instructions') #look into putting this with the other request libraries

            inventory.status = 3
            inventory.pickup_instructions = pickup_instructions # this comes from the FE from onlclick = "updateStatus"

            crud.send_notification(inventory.pickup_user.mobile_number, f'Your {inventory.herb.herb_name} is ready. Get it by: {inventory.pickup_instructions}')

        elif task == 'complete' and inventory.status == 3 and inventory.pickup_user_id == user_id: # only person that requested it can complete pickup
            inventory.status = 4

            crud.send_notification(inventory.user.mobile_number, f'Awesome news! {inventory.pickup_user.fname.strip().title()} picked up your {inventory.herb.herb_name}')

        elif task == 'delete' and inventory.status == 1 and inventory.user_id == user_id: # only currently active item (non requested) and person that posted it can delete a listing
            inventory.status = 0

        elif task == 'cancel' and inventory.status == 2 and inventory.pickup_user_id == user_id:
            inventory.status = 1

            crud.send_notification(inventory.user.mobile_number, f'Nevermind! {inventory.pickup_user.fname.strip().title()} cancelled the request for your {inventory.herb.herb_name}')

        else:
            # non-valid task was passed
            return 'bad request!', 404

        inventory.last_update = datetime.now()
        inventory.update_id = user_id
        db.session.commit()
        return 'success', 200

    else:
        # inventory was not found
        return 'inventory not found!', 404


@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)