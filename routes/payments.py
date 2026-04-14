
from flask import Blueprint, render_template, request, redirect, url_for
from .db_util import get_db

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')

@payments_bp.route('/')
def list_payments():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""SELECT p.*, m.name as member_name FROM Payment p
                   LEFT JOIN Member m ON p.member_id = m.member_id ORDER BY p.payment_date DESC""")
    rows = cur.fetchall(); db.close()
    return render_template('payments/list.html', payments=rows)

@payments_bp.route('/add', methods=['GET','POST'])
def add_payment():
    if request.method=='POST':
        db = get_db(); cur = db.cursor()
        cur.execute("""INSERT INTO Payment (member_id, amount, payment_date, due_date, status)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (request.form['member_id'], request.form['amount'], request.form['payment_date'],
                     request.form['due_date'], request.form['status']))
        db.commit(); db.close()
        return redirect(url_for('payments.list_payments'))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name FROM Member"); members = cur.fetchall(); db.close()
    return render_template('payments/add.html', members=members)
