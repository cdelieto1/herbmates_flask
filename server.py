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
    inventory = Inventory.query.filter_by(status=1, complex_id=user.complex_id)

    return render_template('homepage.html', user=user, inventory=inventory)


@app.route('/signup', methods=['GET', 'POST'])
def register_user():
    """Create a new user."""

    # TODO: get all ACTIVE complexes and POPULATE LIST and sort ALPHABETICALLY in DROPDOWN

    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        complex_id = request.form.get('complex_id')

        if password != confirm_password:
            flash('Passwords do not match. Try again')

        user = crud.get_user_by_email(email)

        if user:
            flash('Cannot create an account')
        else:
            crud.create_user(email, password)
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


@app.route('/herb_add/<herb_id>')
def add_herbs(herb_id):
    """Add an herb"""

    herbs = crud.get_herbs_in_inventory()

    return redirect('/', herbs=herbs)


@app.route('/herb_requested/<herb_id>')
def delete_herbs(herb_id):
    """Delete an herb"""

    herbs = crud.msg_herb_owner_id(movie_id)

    return redirect('/', movie=movie)



@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)