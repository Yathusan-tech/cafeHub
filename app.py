"""
CafeHub - Cafe Management & Online Ordering System
=====================================================
A complete Flask + SQLite web application built as a college project.

This single file contains:
- Flask app configuration
- SQLite database initialization + sample data seeding
- Customer-facing routes (home, menu, cart, checkout, order tracking, about, contact)
- Admin routes (login, dashboard, menu CRUD, order management)

Python concepts demonstrated (see comments throughout):
variables, functions, conditionals, loops, lists, dictionaries,
exception handling, database operations, Flask routing, sessions, CRUD.
"""

import sqlite3
import os
import random
import string
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, g, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cafehub_secret_key_change_in_production")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "database.db"))

# Default admin credentials (configurable via environment variables)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# Valid order statuses (a Python list, used for validation and dropdowns)
ORDER_STATUSES = ["Pending", "Preparing", "Ready", "Completed", "Cancelled"]

# Valid menu categories (a Python list)
MENU_CATEGORIES = ["Coffee", "Tea", "Snacks", "Desserts"]


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db():
    """
    Returns a SQLite connection stored on Flask's 'g' object so that only
    one connection is opened per request (a common Flask pattern).
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # lets us access columns by name
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    """Automatically closes the database connection after each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """
    Creates all required tables if they do not already exist, and inserts
    sample menu items only the first time the application is run.
    This function demonstrates DDL (CREATE TABLE) and conditional seeding.
    """
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # ---- menu_items table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            available INTEGER NOT NULL DEFAULT 1
        )
    """)

    # ---- orders table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT NOT NULL UNIQUE,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            table_number TEXT NOT NULL,
            special_instructions TEXT,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)

    # ---- order_items table (foreign keys -> orders, menu_items) ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
        )
    """)

    conn.commit()

    # ---- Seed sample menu items only if table is empty ----
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    count = cursor.fetchone()[0]

    if count == 0:
        # A Python list of dictionaries/tuples describing sample items.
        # SVG placeholder images are referenced via /static/images/placeholder.svg
        # generated dynamically per category using an emoji-based SVG (see below).
        sample_items = [
            # (name, description, category, price, image, available)
            ("Espresso", "Strong and bold single shot of pure coffee.", "Coffee", 90, "espresso.svg", 1),
            ("Cappuccino", "Espresso topped with steamed milk foam.", "Coffee", 130, "cappuccino.svg", 1),
            ("Latte", "Smooth espresso with silky steamed milk.", "Coffee", 140, "latte.svg", 1),
            ("Mocha", "Espresso blended with chocolate and milk.", "Coffee", 150, "mocha.svg", 1),
            ("Americano", "Espresso diluted with hot water.", "Coffee", 110, "americano.svg", 1),
            ("Cold Coffee", "Chilled coffee blended with ice cream.", "Coffee", 160, "coldcoffee.svg", 1),

            ("Masala Tea", "Classic Indian spiced milk tea.", "Tea", 50, "masalatea.svg", 1),
            ("Green Tea", "Light and healthy antioxidant-rich tea.", "Tea", 60, "greentea.svg", 1),
            ("Lemon Tea", "Refreshing tea with a hint of lemon.", "Tea", 55, "lemontea.svg", 1),
            ("Ginger Tea", "Warm tea infused with fresh ginger.", "Tea", 55, "gingertea.svg", 1),

            ("Veg Sandwich", "Fresh vegetables layered in toasted bread.", "Snacks", 90, "vegsandwich.svg", 1),
            ("Cheese Sandwich", "Melted cheese with grilled veggies.", "Snacks", 110, "cheesesandwich.svg", 1),
            ("French Fries", "Crispy golden fries served with ketchup.", "Snacks", 100, "fries.svg", 1),
            ("Veg Burger", "Loaded veggie patty burger with fresh toppings.", "Snacks", 120, "burger.svg", 1),
            ("Pasta", "Creamy Italian style pasta.", "Snacks", 150, "pasta.svg", 1),

            ("Chocolate Cake", "Rich and moist chocolate sponge cake.", "Desserts", 120, "chocolatecake.svg", 1),
            ("Brownie", "Fudgy chocolate brownie served warm.", "Desserts", 90, "brownie.svg", 1),
            ("Donut", "Soft glazed donut with sweet topping.", "Desserts", 70, "donut.svg", 1),
            ("Ice Cream", "Creamy vanilla ice cream scoop.", "Desserts", 80, "icecream.svg", 1),
            ("Cheesecake", "Smooth and creamy classic cheesecake.", "Desserts", 160, "cheesecake.svg", 1),
        ]

        # Loop through the list and insert each item (demonstrates for-loop + params)
        for item in sample_items:
            cursor.execute("""
                INSERT INTO menu_items (name, description, category, price, image, available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, item)

        conn.commit()
        print("Sample menu items inserted.")
    else:
        print("Menu items already exist. Skipping sample data insertion.")

    # ---- admins table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    # ---- Seed default admin account with hashed password if empty ----
    cursor.execute("SELECT COUNT(*) FROM admins")
    admin_count = cursor.fetchone()[0]
    if admin_count == 0:
        default_user = os.environ.get("ADMIN_USERNAME", "admin")
        default_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
        cursor.execute("""
            INSERT INTO admins (username, password_hash, created_at)
            VALUES (?, ?, ?)
        """, (default_user, generate_password_hash(default_pass), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        print(f"Default admin '{default_user}' created with secure password hash.")

    conn.close()


# Initialize database automatically on startup
try:
    init_db()
except Exception as _e:
    pass


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------
def generate_order_number():
    """Generates a unique order number like CH-20260827-XXXX."""
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = "".join(random.choices(string.digits + string.ascii_uppercase, k=4))
    return f"CH-{date_part}-{random_part}"


def get_cart():
    """
    Returns the cart dictionary stored in the Flask session.
    Cart structure: { "<menu_item_id>": quantity, ... }
    Using session keeps the cart tied to each visitor's browser
    without needing a login.
    """
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}
    return session["cart"]


def get_cart_details():
    """
    Builds a detailed list of cart items (with name, price, subtotal etc.)
    by joining the session cart data with the menu_items table.
    Also computes total item count and grand total.
    """
    cart = get_cart()
    db = get_db()
    items = []
    total_items = 0
    grand_total = 0.0

    # Loop through each entry in the cart dictionary
    for item_id, qty in cart.items():
        try:
            item_id_int = int(item_id)
            qty_int = int(qty)
        except (ValueError, TypeError):
            continue  # skip corrupted cart entries

        menu_item = db.execute(
            "SELECT * FROM menu_items WHERE id = ?", (item_id_int,)
        ).fetchone()

        if menu_item is None:
            continue  # item may have been deleted by admin

        subtotal = menu_item["price"] * qty_int
        items.append({
            "id": menu_item["id"],
            "name": menu_item["name"],
            "price": menu_item["price"],
            "image": menu_item["image"],
            "quantity": qty_int,
            "subtotal": subtotal
        })
        total_items += qty_int
        grand_total += subtotal

    return items, total_items, grand_total


def login_required(f):
    """
    Decorator that protects admin routes.
    If the admin is not logged in, redirect to the admin login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access the admin area.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


@app.context_processor
def inject_cart_count():
    """
    Makes the cart item count available in every template automatically,
    so the navbar cart icon can always show an up-to-date count.
    """
    cart = session.get("cart", {})
    count = 0
    for qty in cart.values():
        try:
            count += int(qty)
        except (ValueError, TypeError):
            pass
    return {"cart_count": count}


# ---------------------------------------------------------------------------
# Customer-facing routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Homepage: shows featured menu items."""
    db = get_db()
    featured_items = db.execute("""
        SELECT * FROM menu_items 
        WHERE available = 1 
        ORDER BY CASE 
            WHEN name = 'Cappuccino' THEN 1
            WHEN name IN ('Cold Mocha', 'Mocha') THEN 2
            WHEN name IN ('Classic Burger', 'Veg Burger') THEN 3
            WHEN name IN ('Creamy Pasta', 'Pasta') THEN 4
            WHEN name IN ('Choco Lava Cake', 'Chocolate Cake') THEN 5
            ELSE 6
        END, id ASC
        LIMIT 5
    """).fetchall()
    return render_template("index.html", featured_items=featured_items)


@app.route("/menu")
def menu():
    """Menu page: shows all available items. Filtering/sorting is done client-side with JS,
    but we also support a basic server-side category filter via query string for robustness."""
    db = get_db()
    category = request.args.get("category", "All")

    if category and category != "All":
        items = db.execute(
            "SELECT * FROM menu_items WHERE category = ? ORDER BY name", (category,)
        ).fetchall()
    else:
        items = db.execute("SELECT * FROM menu_items ORDER BY category, name").fetchall()

    return render_template("menu.html", items=items, categories=MENU_CATEGORIES, selected_category=category)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    """Adds an item to the cart, or increases its quantity if already present."""
    item_id = request.form.get("item_id")
    quantity = request.form.get("quantity", "1")

    db = get_db()
    menu_item = db.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()

    if menu_item is None:
        flash("Invalid menu item.", "error")
        return redirect(url_for("menu"))

    if not menu_item["available"]:
        flash(f"{menu_item['name']} is currently unavailable.", "error")
        return redirect(url_for("menu"))

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    cart = get_cart()
    current_qty = int(cart.get(item_id, 0))
    cart[item_id] = current_qty + quantity
    session["cart"] = cart
    session.modified = True

    flash(f"{menu_item['name']} added to cart!", "success")
    return redirect(request.referrer or url_for("menu"))


@app.route("/cart")
def cart():
    """Displays the shopping cart with all items, quantities and totals."""
    items, total_items, grand_total = get_cart_details()
    return render_template("cart.html", items=items, total_items=total_items, grand_total=grand_total)


@app.route("/update-cart", methods=["POST"])
def update_cart():
    """Updates the quantity of a specific item in the cart (increase/decrease)."""
    item_id = request.form.get("item_id")
    action = request.form.get("action")  # "increase" or "decrease"

    cart = get_cart()

    if item_id in cart:
        qty = int(cart[item_id])
        if action == "increase":
            qty += 1
        elif action == "decrease":
            qty -= 1

        if qty <= 0:
            cart.pop(item_id, None)
        else:
            cart[item_id] = qty

        session["cart"] = cart
        session.modified = True

    return redirect(url_for("cart"))


@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    """Removes a single item entirely from the cart."""
    item_id = request.form.get("item_id")
    cart = get_cart()
    cart.pop(item_id, None)
    session["cart"] = cart
    session.modified = True
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart"))


@app.route("/clear-cart", methods=["POST"])
def clear_cart():
    """Empties the entire cart."""
    session["cart"] = {}
    session.modified = True
    flash("Cart cleared.", "success")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET"])
def checkout():
    """Shows the checkout form along with an order summary."""
    items, total_items, grand_total = get_cart_details()

    if not items:
        flash("Your cart is empty. Add items before checking out.", "error")
        return redirect(url_for("menu"))

    return render_template("checkout.html", items=items, total_items=total_items, grand_total=grand_total)


@app.route("/place-order", methods=["POST"])
def place_order():
    """
    Validates checkout form data, saves the order + order items to SQLite,
    clears the cart, and redirects to the confirmation page.
    """
    items, total_items, grand_total = get_cart_details()

    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("menu"))

    # ---- Collect and validate form fields ----
    customer_name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    table_number = request.form.get("table_number", "").strip()
    special_instructions = request.form.get("special_instructions", "").strip()

    errors = []
    if not customer_name:
        errors.append("Full name is required.")
    
    phone_clean = phone.replace(" ", "").replace("-", "").replace("+91", "").replace("+", "")
    if not phone_clean or not phone_clean.isdigit() or len(phone_clean) < 10:
        errors.append("A valid 10-digit mobile number is required.")
    if not table_number:
        errors.append("Table number is required.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("checkout"))

    # ---- Save order to database (try/except with retry for robust error handling) ----
    db = get_db()
    order_number = generate_order_number()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_saved = False
    for _ in range(3):
        try:
            cursor = db.execute("""
                INSERT INTO orders
                    (order_number, customer_name, phone, email, table_number,
                     special_instructions, total_amount, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
            """, (order_number, customer_name, phone, email, table_number,
                  special_instructions, grand_total, created_at))

            order_id = cursor.lastrowid

            # Save each cart item as an order_item row
            for item in items:
                db.execute("""
                    INSERT INTO order_items (order_id, menu_item_id, item_name, quantity, price)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, item["id"], item["name"], item["quantity"], item["price"]))

            db.commit()
            order_saved = True
            break
        except sqlite3.IntegrityError:
            db.rollback()
            order_number = generate_order_number()
        except sqlite3.Error:
            db.rollback()
            break

    if not order_saved:
        flash("Something went wrong while placing your order. Please try again.", "error")
        return redirect(url_for("checkout"))

    # Clear the cart after a successful order
    session["cart"] = {}
    session.modified = True

    return redirect(url_for("order_success", order_number=order_number))


@app.route("/order/<order_number>")
def order_success(order_number):
    """Shows the order confirmation page for a given order number."""
    db = get_db()
    order = db.execute(
        "SELECT * FROM orders WHERE order_number = ?", (order_number,)
    ).fetchone()

    if order is None:
        abort(404)

    order_items = db.execute(
        "SELECT * FROM order_items WHERE order_id = ?", (order["id"],)
    ).fetchall()

    return render_template("order_success.html", order=order, order_items=order_items)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Displays the contact page and handles (mock) contact form submission."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
        else:
            # In a real app this would send an email or save to DB.
            flash("Thank you! Your message has been sent successfully.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Secure Admin Portal Login with password hash verification."""
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db()
        admin = db.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()

        if admin and check_password_hash(admin["password_hash"], password):
            session["admin_logged_in"] = True
            session["admin_username"] = admin["username"]
            session["admin_id"] = admin["id"]
            flash(f"Welcome back, {admin['username']}!", "success")
            return redirect(url_for("admin_dashboard"))
        elif not admin and username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Fallback for first-time environment admin setup
            new_hash = generate_password_hash(ADMIN_PASSWORD)
            db.execute("INSERT OR REPLACE INTO admins (username, password_hash, created_at) VALUES (?, ?, ?)",
                       (ADMIN_USERNAME, new_hash, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()
            session["admin_logged_in"] = True
            session["admin_username"] = ADMIN_USERNAME
            flash(f"Welcome back, {ADMIN_USERNAME}!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    """Destroys admin session upon logout."""
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    session.pop("admin_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin/settings", methods=["GET", "POST"])
@login_required
def admin_settings():
    """Allows administrators to update their password securely."""
    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_password or not new_password or not confirm_password:
            flash("All password fields are required.", "error")
            return render_template("admin/settings.html")

        if new_password != confirm_password:
            flash("New passwords do not match.", "error")
            return render_template("admin/settings.html")

        if len(new_password) < 6:
            flash("New password must be at least 6 characters.", "error")
            return render_template("admin/settings.html")

        db = get_db()
        admin_user = session.get("admin_username", ADMIN_USERNAME)
        admin = db.execute("SELECT * FROM admins WHERE username = ?", (admin_user,)).fetchone()

        if not admin or not check_password_hash(admin["password_hash"], current_password):
            flash("Current password is incorrect.", "error")
            return render_template("admin/settings.html")

        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE admins SET password_hash = ? WHERE id = ?", (new_hash, admin["id"]))
        db.commit()

        flash("Password updated successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/settings.html")


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    db = get_db()

    total_menu_items = db.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0]
    total_orders = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    pending_orders = db.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'Pending'"
    ).fetchone()[0]
    preparing_orders = db.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'Preparing'"
    ).fetchone()[0]
    ready_orders = db.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'Ready'"
    ).fetchone()[0]
    completed_orders = db.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'Completed'"
    ).fetchone()[0]
    cancelled_orders = db.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'Cancelled'"
    ).fetchone()[0]
    total_sales_row = db.execute(
        "SELECT SUM(total_amount) FROM orders WHERE status != 'Cancelled'"
    ).fetchone()[0]
    total_sales = total_sales_row if total_sales_row else 0

    recent_orders = db.execute(
        "SELECT * FROM orders ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    return render_template(
        "admin/dashboard.html",
        total_menu_items=total_menu_items,
        total_orders=total_orders,
        pending_orders=pending_orders,
        preparing_orders=preparing_orders,
        ready_orders=ready_orders,
        completed_orders=completed_orders,
        cancelled_orders=cancelled_orders,
        total_sales=total_sales,
        recent_orders=recent_orders
    )


@app.route("/admin/menu")
@login_required
def admin_menu():
    db = get_db()
    items = db.execute("SELECT * FROM menu_items ORDER BY category, name").fetchall()
    return render_template("admin/menu.html", items=items)


@app.route("/admin/menu/add", methods=["GET", "POST"])
@login_required
def admin_add_menu():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "").strip()
        image = request.form.get("image", "").strip()
        available = 1 if request.form.get("available") == "on" else 0

        errors = []
        if not name:
            errors.append("Item name is required.")
        if category not in MENU_CATEGORIES:
            errors.append("Please choose a valid category.")
        try:
            price = float(price)
            if price <= 0:
                errors.append("Price must be greater than zero.")
        except ValueError:
            errors.append("Price must be a valid number.")
            price = 0

        if not image:
            image = "placeholder.svg"

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("admin/add_menu.html", categories=MENU_CATEGORIES, form=request.form)

        db = get_db()
        db.execute("""
            INSERT INTO menu_items (name, description, category, price, image, available)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, category, price, image, available))
        db.commit()

        flash(f"'{name}' added to the menu.", "success")
        return redirect(url_for("admin_menu"))

    return render_template("admin/add_menu.html", categories=MENU_CATEGORIES, form={})


@app.route("/admin/menu/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def admin_edit_menu(item_id):
    db = get_db()
    item = db.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()

    if item is None:
        flash("Menu item not found.", "error")
        return redirect(url_for("admin_menu"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "").strip()
        image = request.form.get("image", "").strip()
        available = 1 if request.form.get("available") == "on" else 0

        errors = []
        if not name:
            errors.append("Item name is required.")
        if category not in MENU_CATEGORIES:
            errors.append("Please choose a valid category.")
        try:
            price = float(price)
            if price <= 0:
                errors.append("Price must be greater than zero.")
        except ValueError:
            errors.append("Price must be a valid number.")
            price = 0

        if not image:
            image = "placeholder.svg"

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("admin/edit_menu.html", item=item, categories=MENU_CATEGORIES)

        db.execute("""
            UPDATE menu_items
            SET name = ?, description = ?, category = ?, price = ?, image = ?, available = ?
            WHERE id = ?
        """, (name, description, category, price, image, available, item_id))
        db.commit()

        flash(f"'{name}' updated successfully.", "success")
        return redirect(url_for("admin_menu"))

    return render_template("admin/edit_menu.html", item=item, categories=MENU_CATEGORIES)


@app.route("/admin/menu/delete/<int:item_id>", methods=["POST"])
@login_required
def admin_delete_menu(item_id):
    db = get_db()
    item = db.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()

    if item is None:
        flash("Menu item not found.", "error")
    else:
        try:
            db.execute("UPDATE order_items SET menu_item_id = NULL WHERE menu_item_id = ?", (item_id,))
            db.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
            db.commit()
            flash(f"'{item['name']}' deleted from the menu.", "success")
        except sqlite3.Error:
            db.rollback()
            flash("Could not delete menu item due to a database error.", "error")

    return redirect(url_for("admin_menu"))


@app.route("/admin/menu/toggle/<int:item_id>", methods=["POST"])
@login_required
def admin_toggle_menu(item_id):
    """Toggles the availability of a menu item between available/unavailable."""
    db = get_db()
    item = db.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()

    if item is None:
        flash("Menu item not found.", "error")
    else:
        new_status = 0 if item["available"] else 1
        db.execute("UPDATE menu_items SET available = ? WHERE id = ?", (new_status, item_id))
        db.commit()
        flash(f"'{item['name']}' availability updated.", "success")

    return redirect(url_for("admin_menu"))


@app.route("/admin/orders")
@login_required
def admin_orders():
    db = get_db()
    status_filter = request.args.get("status", "All")

    if status_filter and status_filter != "All":
        orders = db.execute(
            "SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC", (status_filter,)
        ).fetchall()
    else:
        orders = db.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()

    return render_template(
        "admin/orders.html", orders=orders, statuses=ORDER_STATUSES, selected_status=status_filter
    )


@app.route("/admin/orders/<int:order_id>")
@login_required
def admin_order_details(order_id):
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

    if order is None:
        flash("Order not found.", "error")
        return redirect(url_for("admin_orders"))

    order_items = db.execute(
        "SELECT * FROM order_items WHERE order_id = ?", (order_id,)
    ).fetchall()

    return render_template(
        "admin/order_details.html", order=order, order_items=order_items, statuses=ORDER_STATUSES
    )


@app.route("/admin/orders/<int:order_id>/status", methods=["POST"])
@login_required
def admin_update_order_status(order_id):
    new_status = request.form.get("status")

    if new_status not in ORDER_STATUSES:
        flash("Invalid status value.", "error")
        return redirect(url_for("admin_order_details", order_id=order_id))

    db = get_db()
    db.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    db.commit()

    flash("Order status updated.", "success")
    return redirect(url_for("admin_order_details", order_id=order_id))


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os

    init_db()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )