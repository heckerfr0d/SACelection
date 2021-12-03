from flask import request, render_template, redirect, url_for, jsonify
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from . import db
import datetime


@app.route('/')
def root():
    #returning the template for the index page with the variable election to check if we should show the results button
    return render_template('index.html',election=db.hide_results())


@app.route('/login/', methods=['POST'])
def login():
    user = db.auth(request.form.get('email'), request.form.get('password')) ##authenticating the user
    if user:
        if user.get_status() == -1: # checking if user is an admin
            if not db.get_running_election(): # redirecting to admin page if there are no active elections
                login_user(user)
                return redirect(url_for('admin'))
            return render_template('index.html', message="Election is already running",election=db.hide_results()) #redirecting back to index page as admin cant log in while there is an active election
        elif db.get_running_election():#redirecting the voter to voting page if there is an active election
            login_user(user)
            return redirect(url_for('vote'))
        return render_template('index.html', message="Election is not active",election=db.hide_results())
    return render_template('index.html', message="Invalid Credentials", election = db.hide_results()) #prompting user to enter correct credentials



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
    if current_user.get_status() != -1:
        user_id = current_user.get_id()
        election_id = db.get_running_election() #getting the active election id
        if request.method == 'POST':
            resp = request.get_json()
            result = db.modify_votes(resp['can_email'], user_id, election_id)# updating the number of votes for the candidate
        candidates = {}
        for i in range(1, 11):
            if not db.check_if_voted(user_id, i) : #checking if the user has voted for that position
                candidates[i] = db.cur_candidates(i, election_id) #getting candidates for each position
            else:
                candidates[i] = [('Vote registered','Invalid')]
        positions = db.get_positions() #getting the position's details
        #redirecting user to the voting page with positions and candidates passed in
        return render_template('vote.html', user_id=user_id, packed=zip(positions, list(candidates.values())))
    logout_user()
    return render_template('index.html', message="Admins cannot vote!",election=db.hide_results())


@app.route('/results/', methods=['GET'])
def result():
    # elections = db.get_elections()
    # election_id = max([i[0]
    #                   for i in elections if datetime.datetime.now() > i[2]])
    # candidates = {}
    # for i in range(1, 11):
    #     candidates[i] = db.cur_candidate_votes(i, election_id)
    #     if candidates[i]:
    #         candidates[i] = [(max(candidates[i], key=lambda x:x[1])[0],)]
    #     else:
    #         candidates[i] = [('No candidates participated',)]
    # positions = db.get_positions()
    if not db.hide_results(): # checking if the results button is shown
        results = db.get_results() # getting result data
        return render_template('results.html', packed=results)
    return render_template('index.html', message="No results to display",election=db.hide_results())


@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.get_status() != -1: #verifying the user is an admin
        logout_user()
        return render_template('index.html', message="Only admins can access that page",election=db.hide_results())

    if db.get_running_election(): # verifying there is no activate election
        logout_user()
        return render_template('index.html', message="Election is already running",election=db.hide_results())

    if request.method == 'POST': 
        db.set_election(request.form['start'],
                        request.form['end'], current_user.get_id())
        #getting candidate and position details
        election_details = db.get_upcoming_election_details()
        candidates = {}
        for i in range(1, 11):
            candidates[i] = db.get_candidate_position(i)

        positions = db.get_positions()
        return render_template('admin.html', election_id=election_details[0], election_details=election_details, packed=zip(positions, list(candidates.values())))
    #getting election_details
    election_details = db.get_upcoming_election_details()
    if not election_details: #if no election the redirecting to schedule election page
        election_details = [-1, datetime.datetime.now(),
                            datetime.datetime.now()]
        return render_template('election.html', election_details=election_details, election_id=-1)

    candidates = {}
    for i in range(1, 11):
        candidates[i] = db.get_candidate_position(i)
    positions = db.get_positions()
    return render_template('admin.html', election_id=election_details[0], election_details=election_details, packed=zip(positions, list(candidates.values())))


@app.route('/addcandidate', methods=['POST'])
@login_required
def add_candidate():
    if current_user.get_status() != -1: #verifying user is an admin
        logout_user()
        return jsonify({"error": "unauthorized"})
    resp = request.get_json()
    db.add_candidate(resp['name'], resp['email'], resp['position']) #adding the new candidate to the db
    return jsonify({"test": "sucess"})


@app.route('/deletecandidate', methods=['POST'])
@login_required
def delete_candidate():
    if current_user.get_status() != -1:  #verifying user is an admin
        logout_user()
        return jsonify({"error": "unauthorized"})
    resp = request.get_json()
    db.delete_candidate(resp['email'])  #deleting the candidate from the db
    return jsonify({"test": "sucess"})


@app.route('/deleteallcandidate', methods=['POST'])
@login_required
def delete_all_candidate():
    if current_user.get_status() != -1:
        logout_user()
        return jsonify({"error": "unauthorized"})
    resp = request.get_json()
    db.delete_all_candidates(resp['id']) # deleting all candidates with the postion_id
    return jsonify({"test": "sucess"})


@app.route('/election/<eid>', methods=['GET', 'POST'])
@login_required
def election(eid):
    if current_user.get_status() != -1: 
        logout_user()
        return render_template('index.html', message="Only admins can access that page",election=db.hide_results())
    if request.method == 'GET':
        election_details = db.get_upcoming_election_details() #geting the electin details to modify
        return render_template('election.html', election_id=election_details[0], election_details=election_details, min=datetime.datetime.now())

    else:
        db.modify_election(request.form['start'], request.form['end'], eid) #modifying election start and end datetime
        return redirect(url_for('admin'))
