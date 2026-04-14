
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.route('/')
def list_progress():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""SELECT p.*, m.name as member_name FROM Progress p
                   LEFT JOIN Member m ON p.member_id = m.member_id ORDER BY p.date DESC""")
    rows = cur.fetchall(); db.close()
    return render_template('progress/list.html', records=rows)

@progress_bp.route('/add', methods=['GET','POST'])
def add_progress():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Progress (member_id, date, weight_kg, bmi, body_fat_pct, goal_status)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['date'], request.form['weight_kg'],
                     request.form['bmi'], request.form['body_fat_pct'], request.form['goal_status']))
        db.commit(); db.close()
        return redirect(url_for('progress.list_progress'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('progress/add.html', members=members)
