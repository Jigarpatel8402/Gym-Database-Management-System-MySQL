
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

others_bp = Blueprint('others', __name__, url_prefix='/others')

@others_bp.route('/equipment')
def equipment():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Equipment"); rows = cur.fetchall(); db.close()
    return render_template('others/equipment.html', items=rows)

@others_bp.route('/equipment/add', methods=['GET','POST'])
def add_equipment():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO Equipment (name,type,maintenance_date,condition_status) VALUES (%s,%s,%s,%s)",
                    (request.form['name'], request.form['type'], request.form['maintenance_date'], request.form['condition_status']))
        db.commit(); db.close(); return redirect(url_for('others.equipment'))
    return render_template('others/add_equipment.html')

@others_bp.route('/equipment_usage/add', methods=['GET','POST'])
def add_usage():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO EquipmentUsage (equipment_id, member_id, date, duration, calories_burned)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (request.form['equipment_id'], request.form['member_id'], request.form['date'],
                     request.form['duration'], request.form['calories_burned']))
        db.commit(); db.close(); return redirect(url_for('others.equipment'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT equipment_id, name FROM Equipment"); equipments = cur.fetchall()
    cur.execute("SELECT member_id, name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('others/add_usage.html', equipments=equipments, members=members)

@others_bp.route('/diet/add', methods=['GET','POST'])
def add_diet():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO DietPlan (member_id, meal_type, calories, protein, carbs, fat, date)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['meal_type'], request.form['calories'],
                     request.form['protein'], request.form['carbs'], request.form['fat'], request.form['date']))
        db.commit(); db.close(); return redirect(url_for('others.add_diet'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('others/add_diet.html', members=members)

@others_bp.route('/classes')
def classes():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""SELECT c.*, t.name as trainer_name FROM Class c LEFT JOIN Trainer t ON c.trainer_id = t.trainer_id""")
    rows = cur.fetchall(); db.close()
    return render_template('others/classes.html', classes=rows)

@others_bp.route('/classes/add', methods=['GET','POST'])
def add_class():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Class (trainer_id,name,schedule,duration,max_capacity)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (request.form['trainer_id'], request.form['name'], request.form['schedule'],
                     request.form['duration'], request.form['max_capacity']))
        db.commit(); db.close(); return redirect(url_for('others.classes'))
    db = get_db(); cur = db.cursor(dictionary=True); cur.execute("SELECT trainer_id,name FROM Trainer"); trainers = cur.fetchall(); db.close()
    return render_template('others/add_class.html', trainers=trainers)

@others_bp.route('/enroll', methods=['GET','POST'])
def enroll():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO ClassEnrollment (class_id, member_id, enroll_date) VALUES (%s,%s,%s)""",
                    (request.form['class_id'], request.form['member_id'], request.form['enroll_date']))
        db.commit(); db.close(); return redirect(url_for('others.classes'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT class_id,name FROM Class"); classes = cur.fetchall()
    cur.execute("SELECT member_id,name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('others/enroll.html', classes=classes, members=members)

@others_bp.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Feedback (member_id, trainer_id, rating, comments, date)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['trainer_id'], request.form['rating'],
                     request.form['comments'], request.form['date']))
        db.commit(); db.close(); return redirect(url_for('others.feedback'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id,name FROM Member"); members = cur.fetchall()
    cur.execute("SELECT trainer_id,name FROM Trainer"); trainers = cur.fetchall(); db.close()
    return render_template('others/feedback.html', members=members, trainers=trainers)

@others_bp.route('/health/add', methods=['GET','POST'])
def add_health():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO HealthCheckup (member_id, blood_pressure, heart_rate, sugar_level, checkup_date)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['blood_pressure'], request.form['heart_rate'],
                     request.form['sugar_level'], request.form['checkup_date']))
        db.commit(); db.close(); return redirect(url_for('others.add_health'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id,name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('others/add_health.html', members=members)

@others_bp.route('/notify', methods=['GET','POST'])
def notify():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Notifications (member_id, message, date, status) VALUES (%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['message'], request.form['date'], request.form['status']))
        db.commit(); db.close(); return redirect(url_for('others.notify'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id,name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('others/notify.html', members=members)
