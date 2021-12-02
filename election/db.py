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
    cur.execute(
        "SELECT email_id, password, status FROM users WHERE email_id=%s", (email,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], int(user[2]))
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
        cur.execute("INSERT INTO users (email_id, password, status) VALUES (%s, %s, %s)",
                    (email_id, password, status))
        db.commit()
        cur.close()
        return User(email_id, password, status)
    return None


def set_election(start_datetime, end_datetime, admin):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO election (start_datetime, end_datetime, admin_email) VALUES (%s, %s, %s)",
                (start_datetime, end_datetime, admin))
    db.commit()
    cur.close()


def modify_election(start_datetime, end_datetime, eid):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE election SET start_datetime=%s, end_datetime=%s WHERE election_id=%s",
                (start_datetime, end_datetime, eid))
    db.commit()
    cur.close()


def get_running_election():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT election_id FROM election WHERE start_datetime<=%s AND end_datetime>=%s",
                (datetime.now(), datetime.now()))
    election = cur.fetchone()
    cur.close()
    return election


def get_upcoming_election():
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT election_id FROM election WHERE start_datetime>%s", (datetime.now(),))
    election = cur.fetchone()
    cur.close()
    return election


def get_upcoming_election_details():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM election WHERE start_datetime>%s",
                (datetime.now(),))
    election = cur.fetchone()
    cur.close()
    return election


def get_candidates(election_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT c.name, c.email_id p.position FROM candidate c, position p WHERE c.election_id=%s AND c.position_id=p.position_id ORDER BY p.position_id, c.name", (election_id,))
    candidates = cur.fetchall()
    cur.close()
    packed = {}
    for name, email, position in candidates:
        packed[position] = packed.get(position, []) + [(name, email)]
    return packed


def get_positions():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT position,position_id FROM position ORDER BY position_id")
    positions = cur.fetchall()
    cur.close()
    return positions


def get_candidate_position(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name,email_id FROM candidate where position_id=%s ", (id,))
    candidates = cur.fetchall()
    cur.close()
    return candidates


def cur_candidates(id,elec_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name FROM candidate where position_id=%s AND election_id=%s ORDER BY position_id, name",(id,elec_id))
    candidates = cur.fetchall()
    cur.close()
    return candidates

def cur_candidate_votes(id,elec_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name,votes FROM candidate where position_id=%s AND election_id=%s",(id,elec_id))
    candidates = cur.fetchall()
    cur.close()
    return candidates

def add_candidate(name,email,position):
    db = get_db()
    cur = db.cursor()
    election_id=get_upcoming_election()
    cur.execute("INSERT INTO candidate(email_id,name,votes,position_id,election_id) VALUES (%s,%s,0,%s,%s)",(email,name,position,election_id[0]))
    db.commit()
    cur.close()

def delete_candidate(email):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM candidate WHERE email_id=%s",(email,))
    db.commit()
    cur.close()

def delete_all_candidates(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM candidate WHERE position_id=%s",(id,))
    db.commit()
    cur.close()





def modify_votes(can_name,user_id,elec_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE candidate SET votes=votes+1 where name=%s AND election_id=%s",(can_name,elec_id))
    cur.execute("INSERT INTO votes_for (voter_email,position_id) VALUES (%s,(SELECT position_id FROM candidate where name=%s AND election_id=%s));",(user_id,can_name,elec_id))
    db.commit()
    cur.close()

    return "done"

def check_if_voted(user_id,position_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM votes_for WHERE voter_email=%s AND position_id=%s",(user_id,position_id))

    voted = cur.fetchall()
    cur.close()

    return voted

def get_elections():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM election")

    elections = cur.fetchall()
    cur.close()

    return elections


def hide_results():
    if get_running_election() or not get_elections():
        return True
    return False

def get_results():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT c.name, c.votes, p.position  FROM candidate c, position p WHERE c.election_id=(SELECT election_id FROM election WHERE end_datetime=(SELECT MAX(end_datetime) FROM election WHERE end_datetime<%s)) AND c.position_id=p.position_id AND c.votes=(SELECT MAX(votes) FROM candidate WHERE position_id=c.position_id) ORDER BY p.position_id, c.name",(datetime.now(),))
    results = cur.fetchall()
    cur.close()
    packed = {}
    for name,votes,position in results:
        packed[position] = packed.get(position,[]) + [(name,votes)]
    return packed