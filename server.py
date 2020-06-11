"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
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
    inventory = crud.get_herbs_in_inventory(user.complex_id)

    return render_template('homepage.html', user=user, inventory=inventory)


@app.route('/signup', methods=['GET', 'POST'])
def register_user():
    """Create a new user."""

    # TODO: get all ACTIVE complexes and POPULATE LIST and sort ALPHABETICALLY in DROPDOWN

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


@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)