from flask import request, render_template, redirect, url_for, jsonify
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from . import db
import datetime


@app.route('/')
def root():
    # returning the template for the index page with the variable election to check if we should show the results button
    return render_template('index.html', election=db.hide_results())


@app.route('/login/', methods=['POST'])
def login():
    user = db.auth(request.form.get('email'), request.form.get(
        'password'))  # authenticating the user
    if user:
        active = db.get_running_election()
        if user.get_status() == -1:  # checking if user is an admin
            if not active:  # redirecting to admin page if there are no active elections
                login_user(user)
                return redirect(url_for('admin'))
            # redirecting back to index page as admin cant log in while there is an active election
            return render_template('index.html', message="Election is already running", election=db.hide_results())
        elif active:  # redirecting the voter to voting page if there is an active election
            login_user(user)
            if request.form.get('password') in request.form.get('email'):
                return redirect(url_for('change_password'))
            login_user(user)
            return redirect(url_for('vote'))
        return render_template('index.html', message="Election is not active", election=db.hide_results())
    # prompting user to enter correct credentials
    return render_template('index.html', message="Invalid Credentials", election=db.hide_results())

@app.route('/password/', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('confirm_password'):
            user = db.change_password(current_user.get_id(), request.form.get('password'))
            logout_user()
            login_user(user)
            return redirect(url_for('vote'))
        return render_template('change_password.html', message="Passwords do not match")
    return render_template('change_password.html')

@app.login_manager.user_loader
def user_loader(email_id):
    user = db.get_user(email_id)
    return user


@app.login_manager.unauthorized_handler
def unauth():
    return redirect(url_for('login'))


@app.route('/vote/', methods=['GET', 'POST'])
@login_required
def vote():
    if current_user.get_status() != -1:
        user_id = current_user.get_id()
        election_id = db.get_running_election()  # getting the active election id
        if request.method == 'POST':
            resp = request.get_json()
            # updating the number of votes for the candidate
            result = db.modify_votes(resp['can_email'], user_id, election_id)
        candidates = {}
        for i in range(1, 11):
            # checking if the user has already voted
            if not db.check_if_voted(user_id, i, election_id):
                # getting the candidates for each position
                candidates[i] = db.cur_candidates(i, election_id)
            else:
                candidates[i] = [('Vote registered', 'Invalid')]
        positions = db.get_positions()  # getting the position's details
        # redirecting user to the voting page with positions and candidates passed in
        return render_template('vote.html', user_id=user_id, packed=zip(positions, list(candidates.values())))
    logout_user()
    return render_template('index.html', message="Admins cannot vote!", election=db.hide_results())


@app.route('/results/', methods=['GET'])
def result():
    if not db.hide_results():
        results = db.get_results()
        return render_template('results.html', packed=results)
    return render_template('index.html', message="No results to display", election=db.hide_results())


@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.get_status() != -1:  # verifying the user is an admin
        logout_user()
        return render_template('index.html', message="Only admins can access that page", election=db.hide_results())

    if db.get_running_election():  # verifying there is no active election
        logout_user()
        return render_template('index.html', message="Election is already running", election=db.hide_results())

    if request.method == 'POST':
        if not db.get_upcoming_election():
            db.set_election(request.form['start'],
                            request.form['end'], current_user.get_id())
    # getting election_details
    election_details = db.get_upcoming_election_details()
    if not election_details:  # if no election the redirecting to schedule election page
        election_details = [-1, datetime.datetime.now(),
                            datetime.datetime.now()]
        return render_template('election.html', election_details=election_details, election_id=-1)

    candidates = {}
    for i in range(1, 11):
        candidates[i] = db.cur_candidates(i, election_details[0])
    positions = db.get_positions()
    return render_template('admin.html', election_id=election_details[0], election_details=election_details, packed=zip(positions, list(candidates.values())))


@app.route('/addcandidate', methods=['POST'])
@login_required
def add_candidate():
    if current_user.get_status() != -1 or not db.get_upcoming_election() or db.get_running_election():  # verifying user is an admin
        logout_user()
        return jsonify({"error": "unauthorized"})
    resp = request.get_json()
    # adding the new candidate to the db
    db.add_candidate(resp['name'], resp['email'], resp['position'])
    return jsonify({"test": "sucess"})


@app.route('/deletecandidate', methods=['POST'])
@login_required
def delete_candidate():
    if current_user.get_status() != -1 or not db.get_upcoming_election() or db.get_running_election():  # verifying user is an admin
        logout_user()
        return jsonify({"error": "unauthorized"})
    resp = request.get_json()
    db.delete_candidate(resp['email'])  # deleting the candidate from the db
    return jsonify({"test": "sucess"})


@app.route('/deleteallcandidate', methods=['POST'])
@login_required
def delete_all_candidate():
    if current_user.get_status() != -1 or not db.get_upcoming_election() or db.get_running_election():
        logout_user()
        return jsonify({"error": "unauthorized"})
    resp = request.get_json()
    # deleting all candidates with the postion_id
    db.delete_all_candidates(resp['id'])
    return jsonify({"test": "sucess"})


@app.route('/election/<eid>', methods=['GET', 'POST'])
@login_required
def election(eid):
    if current_user.get_status() != -1:
        logout_user()
        return render_template('index.html', message="Only admins can access that page", election=db.hide_results())
    election_id = db.get_upcoming_election()
    if election_id != eid:
        logout_user()
        return render_template('index.html', message="Invalid election id", election=db.hide_results())
    if request.method == 'GET':
        # geting the electin details to modify
        election_details = db.get_upcoming_election_details()
        return render_template('election.html', election_id=election_details[0], election_details=election_details, min=datetime.datetime.now())

    else:
        # modifying election start and end datetime
        db.modify_election(request.form['start'], request.form['end'], eid)
        return redirect(url_for('admin'))
