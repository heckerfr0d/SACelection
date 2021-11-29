from flask import request, render_template
from flask import current_app as app
from flask_login import login_user, logout_user, current_user, login_required
from . import db

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
    user = db.auth(request.json.get('username'), request.json.get('password'))
    if user:
        login_user(user)
        return "some redirect"
    else:
        return "some error"

@app.route('/view/')
@login_required()
def view():
    election_id = db.get_current_election()
    candidates = db.get_candidates(election_id)
    return "something"

