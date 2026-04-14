
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')

@workouts_bp.route('/')
def list_workouts():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""SELECT wp.*, m.name as member_name FROM WorkoutPlan wp
                   LEFT JOIN Member m ON wp.member_id = m.member_id""")
    rows = cur.fetchall(); db.close()
    return render_template('workouts/list.html', plans=rows)

@workouts_bp.route('/add', methods=['GET','POST'])
def add_workout():
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method=='POST':
        cur = db.cursor()
        cur.execute("""INSERT INTO WorkoutPlan (member_id, exercise, sets, reps, duration, calories_burned)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['exercise'], request.form['sets'],
                     request.form['reps'], request.form['duration'], request.form['calories_burned']))
        db.commit(); db.close()
        return redirect(url_for('workouts.list_workouts'))
    cur.execute("SELECT member_id, name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('workouts/add.html', members=members)

@workouts_bp.route('/delete/<int:id>')
def delete_workout(id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM WorkoutPlan WHERE plan_id=%s",(id,))
    db.commit(); db.close()
    return redirect(url_for('workouts.list_workouts'))
