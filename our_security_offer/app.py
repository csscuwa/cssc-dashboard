import flask
from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import os
import json
import dotenv

# session   ===> user_id        first retrieve from whne user enter correct pass
#           ===> logged_in      first retrieve from when user succeed in login

# Variables from .env file
dotenv.load_dotenv()
# Path
base = os.path.dirname(os.path.realpath(__file__)) + '/'
app = flask.Flask(__name__)
app.permanent_session_lifetime = timedelta(seconds=60)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{base}instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# DB and external Mail initialised
mail = Mail(app)
db = SQLAlchemy(app)

# Database structure 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mfa_code = db.Column(db.String(6))
    mfa_expiry = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    ban_time = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_mfa(self):
        self.mfa_code = None
        self.mfa_expiry = None

    def reset_login_state(self):
        self.login_count = 0
        self.ban_time = None

    def ban(self, minutes=5):
        self.login_count = 0
        self.ban_time = datetime.utcnow() + timedelta(minutes=minutes)

    def is_banned(self):
        return self.ban_time is not None and datetime.utcnow() < self.ban_time

    def is_mfa_expired(self):
        return self.mfa_expiry and self.mfa_expiry < datetime.utcnow()

# Automatively create db if not there with default credentials
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='_________@gmail.com')
        admin.set_password('123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")

# Deploy local run
with app.open_resource('static/events.json') as f:
    data = json.load(f)

def load_door_status():
    with open(f'{base}static/door_status.json', 'r') as f:
        _data = json.load(f)
        return _data

def write_door_status(_data):
    with open(f'{base}/static/door_status.json', 'w') as f:
        json.dump(_data, f)

# Login process
@app.route('/api/auth', methods=['POST'])
def door_auth():
    try:
        _username = request.form.get('username')
        _password = request.form.get('password')
        user = User.query.filter_by(username=_username).first()

        # User found
        if user:
            # Check ban time
            if user.is_banned():
                return flask.jsonify({"error": "⛔ You are temporarily banned from logging in."}), 403

            # Password check
            if user.check_password(_password):
                # Reset fail login count
                user.reset_login_state()

                # MFA code generation and calculation
                code = f"{secrets.randbelow(1000000):06d}"
                user.mfa_code = code
                user.mfa_expiry = datetime.utcnow() + timedelta(minutes=3)
                db.session.commit()

                # Send email
                msg = Message("Your MFA Code", recipients=[user.email])
                msg.body = f"Your MFA verification code is: {code}"
                mail.send(msg)

                # Set session
                session['user_id'] = user.id
                session.permanent = True
                return flask.jsonify({"mfa_required": True})
            else:
                user.login_count += 1
                if user.login_count >= 5:
                    user.ban()
                db.session.commit()
        return flask.jsonify({"logged_in": False})
    # Error catch
    except Exception as e:
        print("❌ AUTH ERROR:", e)
        return flask.jsonify({"error": "internal server error"}), 500

# MFA by 6 digit code
@app.route('/api/verify_mfa', methods=['POST'])
def verify_mfa():
    # Data retrieve from fields and cookies
    input_code = request.form.get('mfa_code')
    user_id = session.get('user_id')

    if not user_id:
        return flask.jsonify({"success": False, "error": "Session expired."}), 400

    user = db.session.get(User, user_id)

    # User exist
    if user:
        if user.is_banned():
            return flask.jsonify({"success": False,"error": "⛔ You are temporarily banned from logging in."}), 403

        # Code match
        if user.mfa_code == input_code:
            # Expiration check
            if not user.is_mfa_expired():
                session['logged_in'] = True
                user.reset_mfa()
                user.reset_login_state()
                db.session.commit()
                return flask.jsonify({"success": True})
            else:
                user.reset_mfa()
                db.session.commit()
                return flask.jsonify({"success": False,"error": "MFA code expired."}), 400

        user.login_count += 1
        if user.login_count >=5 :
            user.ban()
        db.session.commit()
        return flask.jsonify({"success": False, "error": "Invalid MFA code."}), 401
    return flask.jsonify({"success": False, "error": "User not found."}), 404

# Internal UI and management
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    door_status = load_door_status()
    if door_status["door_open"]:
        door_stat = "Open"
    else:
        door_stat = "Closed"

    return flask.render_template('dashboard.html', door_status=door_stat, scrolltext=door_status["scrolltext"])

@app.route('/api/get_events')
def get_events():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))
    return flask.jsonify(data)

# Logout feature for covenience
@app.route('/logout')
def logout():
    session.clear()
    return flask.redirect(flask.url_for('login'))

@app.route('/')
def login():
    if session.get('logged_in'):
        return flask.redirect(flask.url_for('dashboard'))
    return flask.render_template('login.html')

@app.route('/change_password', methods=['POST'])
def change_password():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    current_pw = request.form.get('current_password')
    new_pw = request.form.get('new_password')

    user = db.session.get(User, session.get('user_id'))  # change if dynamic users later

    if user and user.check_password(current_pw):
        user.set_password(new_pw)
        db.session.commit()
        return flask.render_template('dashboard.html',
                                door_status=load_door_status()["door_open"],
                                scrolltext=load_door_status()["scrolltext"],
                                password_message="✅ Password updated successfully",
                                password_success=True)
    else:
        return flask.render_template('dashboard.html',
                                door_status=door_stat,
                                scrolltext=door_status["scrolltext"],
                                password_message="❌ Current password is incorrect",
                                password_success=False)

# API

# Door Status
@app.route('/api/door_status')
def get_door_status():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    return flask.jsonify(load_door_status())

@app.route('/api/open_door')
def open_door():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    _data = load_door_status()
    _data['door_open'] = 1
    write_door_status(_data)
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/close_door')
def close_door():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    _data = load_door_status()
    _data['door_open'] = 0
    write_door_status(_data)
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/scrolltext_update', methods=['POST'])
def scrolltext_update():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    new_scrolltext = request.form.get('scrolltext')
    print(new_scrolltext)
    _data = load_door_status()
    _data["scrolltext"] = new_scrolltext
    write_door_status(_data)

    return flask.redirect(flask.url_for('dashboard'))

@app.before_request
def refresh_session_timeout():
    session.permanent = True

if __name__ == "__main__":
    app.run()
