
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

members_bp = Blueprint('members', __name__, url_prefix='/members')

@members_bp.route('/')
def list_members():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Member")
    rows = cur.fetchall()
    db.close()
    return render_template('members/list.html', members=rows)

@members_bp.route('/add', methods=['GET','POST'])
def add_member():
    if request.method == 'POST':
        data = (request.form['name'], request.form['age'], request.form['gender'],
                request.form['phone'], request.form['email'], request.form['membership_type'])
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Member (name, age, gender, phone, email, membership_type, membership_start)
                       VALUES (%s,%s,%s,%s,%s,%s,CURDATE())""", data)
        db.commit(); db.close()
        return redirect(url_for('members.list_members'))
    return render_template('members/add.html')

@members_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_member(id):
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == 'POST':
        cur.execute("""UPDATE Member SET name=%s, age=%s, gender=%s, phone=%s, email=%s, membership_type=%s
                       WHERE member_id=%s""", (request.form['name'], request.form['age'], request.form['gender'],
                                                  request.form['phone'], request.form['email'], request.form['membership_type'], id))
        db.commit(); db.close()
        return redirect(url_for('members.list_members'))
    cur.execute("SELECT * FROM Member WHERE member_id=%s",(id,))
    member = cur.fetchone(); db.close()
    return render_template('members/edit.html', member=member)

@members_bp.route('/delete/<int:id>')
def delete_member(id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Member WHERE member_id=%s",(id,))
    db.commit(); db.close()
    return redirect(url_for('members.list_members'))

@members_bp.route('/search', methods=['GET','POST'])
def search_member():
    if request.method == 'POST':
        q = request.form['q']
        db = get_db(); cur = db.cursor(dictionary=True)
        cur.execute("""SELECT * FROM Member WHERE name LIKE %s OR phone LIKE %s""", ('%'+q+'%','%'+q+'%'))
        rows = cur.fetchall(); db.close()
        return render_template('members/list.html', members=rows)
    return render_template('members/search.html')
