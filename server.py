"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from datetime import datetime
from model import *
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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
    
    orders = crud.get_completed_orders(user.complex_id)

    return render_template('homepage.html', user=user, inventory_count=inventory_count, inventory=inventory, orders=orders)


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
        #print('>>>>>>>>>>>>>>>>>>>>>>>')
        #print(complex_id)

        if password != confirm_password:
            flash('Passwords do not match. Try again')

        user = crud.get_user_by_email(email)

        if user:
            flash('Cannot create an account')
        else:
            user = crud.create_user(email, password, fname, lname, complex_id)
            session['is_authenticated'] = True
            session['user_id'] = user.user_id
            flash('Account created!')
            return redirect('/')

    complexes = Complex.query.all()

    return render_template('signup.html', complexes=complexes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to Herbmates"""


    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        user = crud.get_user_by_email(email) #just a query to see if they exist
        if user and user.password == password:
            #log me in / create session
            session['is_authenticated'] = True
            session['user_id'] = user.user_id
            return redirect('/')
        else:
            flash('Either email or password are incorrect!')

    return render_template('login.html')


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
    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    #print(user.user_id)
    #print(user.complex_id)

    herb_id = request.form.get('herb')
    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    #print(herb_id)

    listing_date=datetime.now()
    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    #print(listing_date)

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
    
    print(request)

    #replace task and inventory_id w/ ajax data on base.js
    task = request.form.get('task') # pickup, ready, complete, delete
    print(task)
    inventory_id = request.form.get('inventory_id')
    print(inventory_id)



    #write crud function to lookup singular inventory
    inventory = crud.get_herb_by_inventory_id(inventory_id)

    if inventory:

        if task == 'pickup' and inventory.status == 1 and inventory.user_id != user_id: # can't book my own herb. 
            inventory.pickup_user_id = user_id
            inventory.status = 2
            
            # TODO last feature: notify inventory.user_id with email/txt pickup request 
            # Christina says the user_id could be 500 error. Handle a bad input. Look into the flask library for requests. 


        elif task == 'ready' and inventory.status == 2 and inventory.user_id == user_id: # only person who posted it can update pickup instructions and make it available

            pickup_instructions = request.form.get('pickup_instructions')

            inventory.status = 3
            inventory.pickup_instructions = pickup_instructions # from FE

            # TODO: notify inventory.pickup_user_id with email/txt incl. pickup instructions

        elif task == 'complete' and inventory.status == 3 and inventory.pickup_user_id == user_id: # only person that requested it can complete pckup
            inventory.status = 4

            # TODO: notify inventory.user_id with email/txt completed msg


        elif task == 'delete' and inventory.status == 1 and inventory.user_id == user_id: # only currently active item (non requested) and person that posted it can delete a listing
            inventory.status = 0

        elif task == 'cancel' and inventory.status == 2 and inventory.pickup_user_id == user_id:
            inventory.status = 1

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