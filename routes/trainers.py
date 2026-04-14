
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

trainers_bp = Blueprint('trainers', __name__, url_prefix='/trainers')

@trainers_bp.route('/')
def list_trainers():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Trainer"); rows = cur.fetchall(); db.close()
    return render_template('trainers/list.html', trainers=rows)

@trainers_bp.route('/add', methods=['GET','POST'])
def add_trainer():
    if request.method == 'POST':
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO Trainer (name,specialization,phone,email) VALUES (%s,%s,%s,%s)",
                    (request.form['name'], request.form['specialization'], request.form['phone'], request.form['email']))
        db.commit(); db.close()
        return redirect(url_for('trainers.list_trainers'))
    return render_template('trainers/add.html')

@trainers_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_trainer(id):
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method=='POST':
        cur.execute("UPDATE Trainer SET name=%s,specialization=%s,phone=%s,email=%s WHERE trainer_id=%s",
                    (request.form['name'], request.form['specialization'], request.form['phone'], request.form['email'], id))
        db.commit(); db.close()
        return redirect(url_for('trainers.list_trainers'))
    cur.execute("SELECT * FROM Trainer WHERE trainer_id=%s",(id,)); row=cur.fetchone(); db.close()
    return render_template('trainers/edit.html', trainer=row)

@trainers_bp.route('/delete/<int:id>')
def delete_trainer(id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Trainer WHERE trainer_id=%s",(id,))
    db.commit(); db.close()
    return redirect(url_for('trainers.list_trainers'))
