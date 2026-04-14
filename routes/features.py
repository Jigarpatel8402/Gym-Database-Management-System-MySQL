from flask import Blueprint, render_template, request
from .db_util import get_db

features_bp = Blueprint('features', __name__, url_prefix='/features')

# Predefined SQL queries
queries = {
    "top_members": "SELECT m.name, COUNT(a.attendance_id) AS total_days FROM Attendance a JOIN Member m ON a.member_id = m.member_id GROUP BY m.name ORDER BY total_days DESC LIMIT 5;",
    "revenue_by_type": "SELECT m.membership_type, SUM(p.amount) AS total_revenue FROM Payment p JOIN Member m ON p.member_id = m.member_id GROUP BY m.membership_type;",
    "expiring_members": "SELECT name, membership_end FROM Member WHERE membership_end BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);",
    "member_workout" : "SELECT m.name AS member_name, w.exercise, w.sets, w.reps FROM WorkoutPlan w JOIN Member m ON w.member_id = m.member_id;"

}

@features_bp.route('/', methods=['GET', 'POST'])
def show_features():
    result = []
    title = ""
    if request.method == 'POST':
        qname = request.form.get('query')
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute(queries[qname])
        result = cur.fetchall()
        title = qname.replace("_", " ").title()
        db.close()
    return render_template('features.html', result=result, title=title)
