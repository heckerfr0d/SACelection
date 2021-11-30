from flask import request, render_template, redirect, url_for
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from flask_cors import CORS, cross_origin
from . import db
import election

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    print('test')
    user = db.auth(request.json.get('username'), request.json.get('password'))
    if user and (user.get_status==-1 or db.get_running_election()):
        login_user(user)
        return True
    else:
        return False


@app.login_manager.user_loader
def user_loader(email_id):
    user = db.get_user(email_id)
    return user


@app.login_manager.unauthorized_handler
def unauth():
    return redirect(url_for('login', ret=403))

@app.route('/vote/', methods=['GET', 'POST'])
@login_required
def vote():
    if request.method == 'POST':
        return "something in db"
    election_id = db.get_running_election()
    candidates = db.get_candidates(election_id)
    return "something"

@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.get_status() != -1:
        return "some error"
    if request.method == 'POST':
        return "something in db"
    election_id = db.get_upcoming_election()
    candidates = db.get_candidates(election_id)
    return "something"