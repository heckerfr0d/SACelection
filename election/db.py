from flask import current_app, g
from psycopg2 import connect
from datetime import datetime
import hashlib

def get_db():
    if 'db' not in g:
        DATABASE_URL = current_app.config['DATABASE_URL']
        # g.db = connect(DATABASE_URL, sslmode='require')
        g.db = connect(DATABASE_URL)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

class User:
    def __init__(self, email_id, password, status):
        self.email_id = email_id
        self.password = password
        self.status = status
        self.authenticated = True

    def is_active(self):
        return True

    def get_id(self):
        return self.email_id

    def get_status(self):
        return self.status

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

def hash_password(password):
    return hashlib.sha3_256(password.encode()).hexdigest()

def get_user(email):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT email_id, password, status FROM users WHERE email_id=%s", (email,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

def auth(email_id, password):
    user = get_user(email_id)
    if user:
        if user.password == hash_password(password):
            return user
    return None

def add_user(email_id, password, status):
    user = get_user(email_id)
    if user is None:
        db = get_db()
        cur = db.cursor()
        password = hash_password(password)
        cur.execute("INSERT INTO users (email_id, password, status) VALUES (%s, %s, %s)", (email_id, password, status))
        db.commit()
        cur.close()
        return User(email_id, password, status)
    return None

def get_current_election():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT election_id FROM election WHERE end_datetime>%s", (datetime.now(),))
    election = cur.fetchone()
    cur.close()
    return election

def get_candidates(election_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT c.email_id, c.name, p.position FROM candidate c, position p WHERE c.election_id=%s AND c.position_id=p.position_id", (election_id,))
    candidates = cur.fetchall()
    cur.close()
    return candidates

