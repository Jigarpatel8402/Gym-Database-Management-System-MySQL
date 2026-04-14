from flask import Flask, render_template, redirect, request, session, url_for
import mysql.connector
import os
from config import DB_CONFIG

# import blueprints
from routes.members import members_bp
from routes.trainers import trainers_bp
from routes.workouts import workouts_bp
from routes.attendance import attendance_bp
from routes.progress import progress_bp
from routes.payments import payments_bp
from routes.others import others_bp
from routes.features import features_bp
from routes.superai import superai_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)  # New key each restart → old sessions always expire

# Register blueprints
app.register_blueprint(members_bp)
app.register_blueprint(trainers_bp)
app.register_blueprint(workouts_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(others_bp)
app.register_blueprint(features_bp)
app.register_blueprint(superai_bp)

# Enforce login on every route except dashboard, /login and /static
@app.before_request
def require_login():
    allowed = {'login', 'static', 'index'}
    if request.endpoint not in allowed and 'user' not in session:
        return redirect(url_for('login', msg='⚠️ Please login to access this feature.'))
# DB helper for quick admin stats
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    # simple dashboard stats
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM Member")
    total_members = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM Trainer")
    total_trainers = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM Attendance WHERE date = CURDATE()")
    todays_att = cur.fetchone()[0]
    db.close()
    print("Members:", total_members, "Trainers:", total_trainers, "Today:", todays_att)

    return render_template('index.html', total_members=total_members, total_trainers=total_trainers, todays_att=todays_att)

# very simple login for demo (username: admin password: admin123)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u=='jigar' and p=='1234':
            session['user'] = u
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
