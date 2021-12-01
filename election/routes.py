from flask import request, render_template, redirect, url_for
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from flask_cors import CORS, cross_origin
from . import db
import election

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/login/', methods=['POST'])
def login():
    user = db.auth(request.form.get('email'), request.form.get('password'))
    if user:
        if user.get_status()==-1:
            if not db.get_running_election():
                login_user(user)
                return redirect(url_for('admin'))
            return render_template('index.html', message="Election is already running")
        elif db.get_running_election():
            login_user(user)
            return redirect(url_for('vote'))
        return render_template('index.html', message="Election is not active")
    return render_template('index.html', message="Invalid Credentials")


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
    candidates = {}
    for i in range(1,11):
        candidates[i] = db.get_candidate_position_cur_election(i,election_id)
    positions = db.get_positions()
    if candidates:
        return render_template('vote.html', packed =zip(positions,list(candidates.values())))
    return "something"

@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.get_status() != -1:
        return "some error"
    if request.method == 'POST':
        return "something in db"
    election_id = db.get_upcoming_election()
    election_details = db.get_upcoming_election_details()
    candidates = {}
    for i in range(1,11):
        candidates[i] = db.get_candidate_position(i)
    positions = db.get_positions()
    return render_template('admin.html',election_id=election_id,election_details=election_details,packed =zip(positions,list(candidates.values())))

@app.route('/addcandidate',methods=['POST'])
def add_candidate():
    resp = request.get_json()
    ## to be done ##
    return "sucess"
