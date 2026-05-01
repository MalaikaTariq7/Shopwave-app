from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "simple-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


PRODUCTS = [
    {"id": 1, "name": "Blue Notebook", "description": "A simple productivity notebook for your tasks and notes.", "price": "$9.99", "icon": "📘"},
    {"id": 2, "name": "Smart Watch", "description": "Stay on time with a clean, lightweight watch design.", "price": "$49.99", "icon": "⌚"},
    {"id": 3, "name": "Daily Planner", "description": "Organize your day and plan your goals in one place.", "price": "$14.99", "icon": "🖊️"},
    {"id": 4, "name": "Wireless Earbuds", "description": "Compact earbuds with clear sound and long battery life.", "price": "$29.99", "icon": "🎧"},
    {"id": 5, "name": "Travel Mug", "description": "A spill-proof mug to keep drinks hot while on the go.", "price": "$12.99", "icon": "☕"},
    {"id": 6, "name": "Desk Plant", "description": "A low-maintenance plant to brighten up your workspace.", "price": "$7.99", "icon": "🌿"},
    {"id": 7, "name": "Bluetooth Speaker", "description": "Portable speaker with crisp audio and simple controls.", "price": "$24.99", "icon": "🔊"},
    {"id": 8, "name": "Notebook Set", "description": "Three colorful notebooks for notes, ideas, and reminders.", "price": "$19.99", "icon": "📒"},
    {"id": 9, "name": "Desk Lamp", "description": "A modern lamp with adjustable brightness settings.", "price": "$34.99", "icon": "💡"},
    {"id": 10, "name": "Phone Stand", "description": "A stable stand for your phone while you work or watch videos.", "price": "$8.99", "icon": "📱"},
    {"id": 11, "name": "Water Bottle", "description": "A reusable bottle to keep you hydrated all day.", "price": "$11.99", "icon": "💧"},
    {"id": 12, "name": "Portable Charger", "description": "A small power bank to recharge devices on the move.", "price": "$22.99", "icon": "🔋"},
    {"id": 13, "name": "Sticky Notes", "description": "A pack of bright sticky notes for quick reminders.", "price": "$5.99", "icon": "📝"},
    {"id": 14, "name": "Laptop Sleeve", "description": "A slim protective sleeve for laptops up to 15 inches.", "price": "$18.99", "icon": "💼"},
    {"id": 15, "name": "Travel Organizer", "description": "A pouch to keep cords, chargers, and accessories tidy.", "price": "$16.99", "icon": "🧳"},
    {"id": 16, "name": "Yoga Mat", "description": "A soft, non-slip mat for stretching and relaxation.", "price": "$21.99", "icon": "🧘"},
    {"id": 17, "name": "Desk Calendar", "description": "A compact calendar that keeps your schedule visible.", "price": "$10.99", "icon": "📅"},
    {"id": 18, "name": "Scented Candle", "description": "A candle with a calming fragrance for home or office.", "price": "$13.99", "icon": "🕯️"},
    {"id": 19, "name": "Colored Pens", "description": "A set of smooth-writing pens in bright colors.", "price": "$9.49", "icon": "🖊️"},
    {"id": 20, "name": "Laptop Stand", "description": "A ventilated stand for better posture and cooling.", "price": "$27.99", "icon": "💻"},
    {"id": 21, "name": "Noise Mask", "description": "Soft eye mask to help you rest and focus.", "price": "$8.49", "icon": "😌"},
]


def setup():
    init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("register.html", name=name, email=email)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password),
            )
            conn.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email is already registered. Try another email.", "error")
            return render_template("register.html", name=name, email=email)
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("login.html", email=email)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password),
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash("Login failed. Please check your email and password.", "error")
        return render_template("login.html", email=email)

    return render_template("login.html")


def login_required(route_function):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)

    wrapper.__name__ = route_function.__name__
    return wrapper


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as count FROM items WHERE user_id = ?",
        (session["user_id"],),
    )
    total_items = cursor.fetchone()["count"]
    conn.close()
    return render_template(
        "dashboard.html",
        name=session.get("user_name"),
        item_count=total_items,
    )


@app.route("/add-item", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Please enter an item title.", "error")
            return render_template("add_item.html")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (user_id, title) VALUES (?, ?)",
            (session["user_id"], title),
        )
        conn.commit()
        conn.close()

        flash("Item added successfully.", "success")
        return redirect(url_for("items"))

    return render_template("add_item.html")


@app.route("/items")
@login_required
def items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title FROM items WHERE user_id = ?",
        (session["user_id"],),
    )
    item_rows = cursor.fetchall()
    conn.close()
    return render_template("items.html", items=item_rows)


@app.route("/delete-item/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM items WHERE id = ? AND user_id = ?",
        (item_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    flash("Item deleted.", "success")
    return redirect(url_for("items"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    setup()
    app.run(debug=True)
