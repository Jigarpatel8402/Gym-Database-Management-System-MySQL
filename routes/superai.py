from flask import Blueprint, render_template, request
from .db_util import get_db

superai_bp = Blueprint('superai', __name__, url_prefix='/superai')

BLOCKED = ["drop", "truncate", "alter", "delete", "update"]


@superai_bp.route('/', methods=['GET', 'POST'])
def super_ai_console():
    result = None
    error = None
    query = ""

    if request.method == 'POST':
        query = request.form.get("query").strip()
        q_lower = query.lower()

        if any(q_lower.startswith(cmd) for cmd in BLOCKED):
            error = "This query is blocked for safety."
        else:
            try:
                db = get_db()
                cur = db.cursor(dictionary=True)
                cur.execute(query)

                if q_lower.startswith("select"):
                    result = cur.fetchall()
                else:
                    db.commit()
                    result = "Query executed successfully."

            except Exception as e:
                error = str(e)

    return render_template("superai.html", query=query, result=result, error=error)
