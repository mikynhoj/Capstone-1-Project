import requests, os
from secrets import API_SECRET_KEY

from flask import Flask, render_template, jsonify, request, make_response, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Cryptocurrency
from forms import LoginForm, UserAddForm, UserEditForm
from flask_migrate import Migrate

app = Flask(__name__)


CURR_USER_KEY = "curr_user"
API_BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///cryptotime'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'Thisisasecret'
toolbar = DebugToolbarExtension(app)

connect_db(app)

migrate = Migrate(app, db)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#########
def request_crypto():
    """Return all crypto values"""

    key = API_SECRET_KEY
    url = API_BASE_URL
    headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': key,
    }

    params = {'start':'1','limit':'30','convert':'USD'}

    response = requests.get(url, params=params, headers=headers).json()
    print(response["data"])

    coins = response['data']
        
    return coins
#HomePage##########

@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage"""
    if g.user:

        return render_template('home.html')

    return render_template('home-anon.html')


#############

#LOGIN
##########
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    print("User logged in", user.id)


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    print("User logged out")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        # try:
        print("tried signup validation validation")
        user = User.signup(
            username=form.username.data,
            password=form.password.data,
        )
        print("user is ", form.username.data)
        print("password is ", form.password.data)
        db.session.commit()
        print("user has been committed")
        # except IntegrityError as e:
        #     flash("Username already taken", 'danger')
        #     return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        print("tried logging in")
        if user:
            do_login(user)
            print("user is", user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')
        print("login failed. User is ", user)
    return render_template('users/login.html', form=form)

    
@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")
############

#cryptodata#
@app.route('/crypto')
def handle_crypto():
    """handle crypto api data AND INSERTS it into database for it to show"""
    if g.user:

        data = request_crypto()
        for x in data:
            new_data = Cryptocurrency(crypto_name=x['name'], crypto_value=x['symbol'], timestamp=x['quote']['USD']['price'])
            db.session.add(new_data)
            db.session.commit()

        cryptocurrency = (Cryptocurrency.query.order_by(Cryptocurrency.crypto_value.desc()).limit(100).all)

        return render_template('crypto.html', cryptocurrency=cryptocurrency)

    response = request_crypto()
    print("DID NOT ADD INTO THE DATABASE")
    return render_template("crypto.html", res=response)

