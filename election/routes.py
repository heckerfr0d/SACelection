from flask import request, render_template, redirect, url_for,jsonify
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from flask_cors import CORS, cross_origin
from . import db
import election
import datetime


@app.route('/')
def root():
    election=db.get_running_election()
    print()
    return render_template('index.html',election=election)


@app.route('/login/', methods=['POST'])
def login():
    user = db.auth(request.form.get('email'), request.form.get('password'))
    if user:
        if user.get_status() == -1:
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
    user_id = current_user.get_id()
    election_id = db.get_running_election()
    if request.method == 'POST':
        resp = request.get_json()
        result =db.modify_votes(resp['can_name'],user_id,election_id)
        print(result)
        return "something in db"
    candidates = {}
    for i in range(1,11):
        if not db.check_if_voted(user_id,i):
            candidates[i] = db.cur_candidates(i,election_id)
        else:
            candidates[i]=[('Vote registered',)]
    positions = db.get_positions()
    
    return render_template('vote.html',user_id = user_id, packed =zip(positions,list(candidates.values())))



@app.route('/results/', methods=['GET', 'POST'])
@login_required
def result():
    elections = db.get_elections()
    election_id = max([i[0] for i in elections if datetime.datetime.now()>i[2]])
    print(election_id)
    candidates = {}
    for i in range(1,11):
        candidates[i] = db.cur_candidate_votes(i,election_id)
        if candidates[i]:
            candidates[i] = [(max(candidates[i],key=lambda x:x[1])[0],)]
        else:
            candidates[i]= [('No candidates participated',)]
        print(candidates)
    positions = db.get_positions()
    return render_template('results.html', packed =zip(positions,list(candidates.values())))


@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.get_status() != -1:
        return "not admin"

    if request.method == 'POST':
        db.set_election(request.form['start'],
                        request.form['end'], current_user.get_id())

        election_details = db.get_upcoming_election_details()
        candidates = {}
        for i in range(1, 11):
            candidates[i] = db.get_candidate_position(i)

        positions = db.get_positions()

        return render_template('admin.html', election_id=election_details[0], election_details=election_details, packed=zip(positions, list(candidates.values())))

    election_details = db.get_upcoming_election_details()
    if not election_details:
        election_details = [datetime.datetime.now(), datetime.datetime.now()]
        return render_template('election.html', election_details=election_details, election_id=-1)

    candidates = {}
    for i in range(1, 11):
        candidates[i] = db.get_candidate_position(i)
    positions = db.get_positions()
    return render_template('admin.html', election_id=election_details[0], election_details=election_details, packed=zip(positions, list(candidates.values())))


@app.route('/addcandidate', methods=['POST'])
def add_candidate():
    resp = request.get_json()
    db.add_candidate(resp['name'],resp['email'],resp['position'])
    return jsonify({"test":"sucess"})

@app.route('/deletecandidate', methods=['POST'])
def delete_candidate():
    resp = request.get_json()
    db.delete_candidate(resp['email'])
    return jsonify({"test":"sucess"})

@app.route('/deleteallcandidate', methods=['POST'])
def delete_all_candidate():
    resp = request.get_json()
    db.delete_all_candidates(resp['id'])
    return jsonify({"test":"sucess"})


@app.route('/election/<eid>', methods=['GET', 'POST'])
def election(eid):
    if request.method == 'GET':
        election_details = db.get_upcoming_election_details()
        return render_template('election.html', election_id=election_details[0], election_details=election_details)

    else:
        db.modify_election(request.form['start'], request.form['end'], eid)
        return redirect(url_for('admin'))