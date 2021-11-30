from flask import request, render_template, redirect, url_for
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from . import db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return "Register"
    user = db.add_user(request.form.get('username'), request.form.get('password'))
    if user:
        login_user(user)
        return "some redirect"
    else:
        return "some error"

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "Login"
    user = db.auth(request.json.get('username'), request.json.get('password'))
    if user:
        login_user(user)
        return "some redirect"
    else:
        return "some error"


@app.login_manager.user_loader
def user_loader(email_id):
    user = db.get_user(email_id)
    return user


@app.login_manager.unauthorized_handler
def unauth():
    return redirect(url_for('login', ret=403))

@app.route('/view/')
@login_required
def view():
    election_id = db.get_current_election()
    candidates = db.get_candidates(election_id)
    return "something"

