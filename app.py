from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, math, random
from functools import wraps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "busbuddy.db")
app = Flask(__name__, template_folder=os.path.join(ROOT, "frontend"),
            static_folder=os.path.join(ROOT, "frontend", "static"))
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT DEFAULT 'user')""")
        con.execute("""CREATE TABLE IF NOT EXISTS buses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, bus_number TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL, destination TEXT NOT NULL, departure TEXT NOT NULL,
            latitude REAL NOT NULL, longitude REAL NOT NULL, status TEXT DEFAULT 'On time')""")
        count = con.execute("SELECT COUNT(*) FROM buses").fetchone()[0]
        if count == 0:
            sample = [
                ("KA-01-AB-1234","Majestic","Electronic City","08:30",12.9767,77.5713,"On time"),
                ("KA-03-CD-5678","Silk Board","Whitefield","09:00",12.9177,77.6233,"On time"),
                ("KA-05-EF-9012","Hebbal","Banashankari","09:15",13.0358,77.5970,"Delayed"),
                ("KA-51-GH-3456","Kengeri","Majestic","09:30",12.9141,77.4820,"On time")
            ]
            con.executemany("""INSERT INTO buses
                (bus_number,source,destination,departure,latitude,longitude,status)
                VALUES(?,?,?,?,?,?,?)""", sample)
        # Demo administrator: admin@busbuddy.com / Admin123!
        admin = con.execute("SELECT id FROM users WHERE email=?", ("admin@busbuddy.com",)).fetchone()
        if not admin:
            con.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                        ("BusBuddy Admin","admin@busbuddy.com",
                         generate_password_hash("Admin123!"),"admin"))

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Please sign in with an administrator account.", "error")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        if not name or not email or len(password) < 6:
            flash("Enter all details. Password must contain at least 6 characters.", "error")
            return render_template("register.html")
        try:
            with db() as con:
                con.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                            (name,email,generate_password_hash(password)))
            flash("Account created. Please sign in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("That email is already registered.", "error")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        with db() as con:
            user = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session.update(user_id=user["id"], name=user["name"], role=user["role"])
            return redirect(url_for("admin") if user["role"] == "admin" else url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    with db() as con:
        buses = con.execute("SELECT * FROM buses ORDER BY departure").fetchall()
    return render_template("dashboard.html", buses=buses)

@app.route("/routes")
def routes():
    with db() as con:
        buses = con.execute("SELECT * FROM buses ORDER BY source").fetchall()
    return render_template("routes.html", buses=buses)

@app.route("/tracking/<int:bus_id>")
def tracking(bus_id):
    with db() as con:
        bus = con.execute("SELECT * FROM buses WHERE id=?", (bus_id,)).fetchone()
    if not bus:
        flash("Bus not found.", "error")
        return redirect(url_for("routes"))
    return render_template("tracking.html", bus=bus)

@app.route("/api/buses")
def api_buses():
    with db() as con:
        rows = con.execute("SELECT * FROM buses ORDER BY departure").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/bus/<int:bus_id>")
def api_bus(bus_id):
    with db() as con:
        row = con.execute("SELECT * FROM buses WHERE id=?", (bus_id,)).fetchone()
    if not row:
        return jsonify({"error":"Bus not found"}), 404
    bus = dict(row)
    # Demo-only movement: small random change around the saved starting point.
    bus["latitude"] += random.uniform(-0.0015, 0.0015)
    bus["longitude"] += random.uniform(-0.0015, 0.0015)
    bus["eta_minutes"] = random.randint(4, 24)
    return jsonify(bus)

@app.route("/admin", methods=["GET","POST"])
@login_required
@admin_required
def admin():
    if request.method == "POST":
        number = request.form.get("bus_number","").strip().upper()
        source = request.form.get("source","").strip()
        destination = request.form.get("destination","").strip()
        departure = request.form.get("departure","").strip()
        try:
            lat = float(request.form.get("latitude","12.9716"))
            lon = float(request.form.get("longitude","77.5946"))
            with db() as con:
                con.execute("""INSERT INTO buses(bus_number,source,destination,departure,latitude,longitude)
                    VALUES(?,?,?,?,?,?)""", (number,source,destination,departure,lat,lon))
            flash("Bus added successfully.", "success")
        except (ValueError, sqlite3.IntegrityError):
            flash("Could not add bus. Check the details and ensure the bus number is unique.", "error")
        return redirect(url_for("admin"))
    with db() as con:
        buses = con.execute("SELECT * FROM buses ORDER BY id DESC").fetchall()
        users = con.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
    return render_template("admin.html", buses=buses, users=users)

@app.route("/admin/delete/<int:bus_id>", methods=["POST"])
@login_required
@admin_required
def delete_bus(bus_id):
    with db() as con:
        con.execute("DELETE FROM buses WHERE id=?", (bus_id,))
    flash("Bus removed.", "success")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
