
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/')
def list_attendance():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""SELECT a.*, m.name as member_name FROM Attendance a
                   LEFT JOIN Member m ON a.member_id = m.member_id ORDER BY a.date DESC""")
    rows = cur.fetchall(); db.close()
    return render_template('attendance/list.html', records=rows)

@attendance_bp.route('/add', methods=['GET','POST'])
def add_attendance():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Attendance (member_id, date, check_in, check_out)
                       VALUES (%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['date'], request.form['check_in'], request.form['check_out']))
        db.commit(); db.close()
        return redirect(url_for('attendance.list_attendance'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('attendance/add.html', members=members)
