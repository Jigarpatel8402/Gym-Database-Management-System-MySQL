
# Gym Tracker (Medium) - Flask + MySQL

**How to run (local)**
1. Install Python requirements:
   ```bash
   pip install flask mysql-connector-python
   ```
2. Import the database:
   - Run the SQL script `db.sql` in your MySQL server (e.g., using phpMyAdmin or MySQL Workbench).
   - The DB user/password in `config.py` is set to `root` / `1234`. Change if needed.
3. Run the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000

**What this ZIP includes**
- `db.sql` : creates `gymdb` and all 15 tables (with foreign keys).
- `app.py` : main Flask app, registers blueprints and dashboard + auth.
- `config.py` : DB credentials (host, user, password, database).
- `routes/` : blueprint modules for each table (CRUD).
- `templates/` : Jinja templates (simple Bootstrap based).
- `static/` : minimal CSS file.
