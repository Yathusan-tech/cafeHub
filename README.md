# ☕ CafeHub – Cafe Management & Online Ordering System

## 1. Project Title
**CafeHub – Cafe Management & Online Ordering System**

## 2. Project Description
CafeHub is a full-stack web application that digitizes the day-to-day operations of a small café. Customers can browse a digital menu, search and filter items, add items to a cart, and place an order for a specific table — all without creating an account. Café staff (the admin) can manage the menu, view incoming orders, and update order status in real time through a dedicated admin panel.

The project is built entirely with **Python (Flask)** on the backend and **SQLite** as the database, with a **Bootstrap 5 + HTML/CSS/JavaScript** frontend — making it simple to set up, run, and explain in a college viva.

## 3. Objectives
- Build a working end-to-end web application using Flask and SQLite.
- Demonstrate core web development concepts: routing, templating, sessions, and CRUD operations.
- Provide a real-world use case (café ordering) that is easy to relate to and demo.
- Practice database design with related tables (menu items, orders, order items).
- Implement both a customer-facing site and a protected admin dashboard.

## 4. Features

**Customer Side**
- Modern, responsive café-themed homepage with hero section, featured items, and testimonials
- Interactive digital menu with images, descriptions, and prices
- Live client-side search, category filter, and price sorting (no page reload)
- Shopping cart with quantity increase/decrease, item removal, and clear-cart
- Checkout form with validation (name, phone, table number)
- Automatic order number generation and order confirmation page
- About and Contact pages with a working (mock) contact form

**Admin Side**
- Secure admin login/logout using Flask sessions
- Dashboard with key stats: total menu items, total orders, pending/completed orders, total sales
- Full menu CRUD: add, edit, delete, and toggle availability of items
- Order management with status filtering (Pending, Preparing, Ready, Completed, Cancelled)
- Order details page to view customer info, items, and update order status

**General**
- Fully responsive design (desktop, tablet, mobile)
- SQLite database auto-created and seeded with sample data on first run
- Parameterized SQL queries (protection against SQL injection)
- Graceful error handling (empty cart, invalid items, unauthorized access, invalid order numbers)

## 5. Technologies Used
| Layer      | Technology                          |
|------------|--------------------------------------|
| Backend    | Python 3, Flask                      |
| Database   | SQLite                               |
| Frontend   | HTML5, CSS3, JavaScript, Jinja2      |
| UI Toolkit | Bootstrap 5 (via CDN)                |
| Sessions   | Flask's built-in session (cookie-based) |

## 6. Folder Structure
```
CafeHub/
│
├── app.py                     # Main Flask application (routes, DB logic)
├── database.db                # SQLite database (auto-created on first run)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── static/
│   ├── css/
│   │   └── style.css          # Café-themed responsive stylesheet
│   ├── js/
│   │   └── script.js          # Menu search/filter/sort logic
│   └── images/                # SVG placeholder images for menu items
│
└── templates/
    ├── base.html               # Shared layout (navbar, footer, flash messages)
    ├── index.html               # Homepage
    ├── menu.html                 # Digital menu with search/filter/sort
    ├── cart.html                  # Shopping cart
    ├── checkout.html               # Checkout form + order summary
    ├── order_success.html           # Order confirmation
    ├── about.html                    # About page
    ├── contact.html                   # Contact page
    ├── 404.html / 500.html             # Error pages
    │
    └── admin/
        ├── login.html            # Admin login
        ├── admin_base.html        # Shared admin layout with sidebar
        ├── dashboard.html           # Admin dashboard with stats
        ├── menu.html                  # Menu management list
        ├── add_menu.html                # Add menu item form
        ├── edit_menu.html                 # Edit menu item form
        ├── orders.html                      # Order management list
        └── order_details.html                # Single order detail + status update
```

## 7. Installation Instructions
1. Make sure Python 3.8+ is installed on your machine.
2. Extract/copy the `CafeHub` folder to your computer.
3. Open a terminal inside the `CafeHub` folder.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 8. How to Run
```bash
python app.py
```
Then open your browser and go to:
```
http://127.0.0.1:5000
```
The SQLite database (`database.db`) is created automatically the first time you run the app, and sample menu items are inserted only once (they won't be duplicated on subsequent runs).

## 9. Database Explanation
CafeHub uses **SQLite**, a lightweight file-based database — perfect for a college project since it needs no separate server.

**`menu_items`** — stores every food/drink item (id, name, description, category, price, image, available)

**`orders`** — stores each customer order (id, order_number, customer_name, phone, email, table_number, special_instructions, total_amount, status, created_at)

**`order_items`** — stores individual line items belonging to an order (id, order_id, menu_item_id, item_name, quantity, price). This table has foreign keys to both `orders` and `menu_items`, forming a classic one-to-many relationship.

## 10. Admin Login Credentials
```
Username: admin
Password: admin123
```

## 11. Main Routes
**Customer routes**
```
GET  /                         Homepage
GET  /menu                     Digital menu (supports ?category=)
POST /add-to-cart               Add item to cart
GET  /cart                      View cart
POST /update-cart                Increase/decrease quantity
POST /remove-from-cart             Remove item from cart
POST /clear-cart                    Empty the cart
GET  /checkout                       Checkout form
POST /place-order                     Save order to database
GET  /order/<order_number>             Order confirmation
GET  /about                             About page
GET/POST /contact                        Contact page + form
```

**Admin routes**
```
GET/POST /admin/login
GET      /admin/logout
GET      /admin/dashboard
GET      /admin/menu
GET/POST /admin/menu/add
GET/POST /admin/menu/edit/<id>
POST     /admin/menu/delete/<id>
POST     /admin/menu/toggle/<id>
GET      /admin/orders               (supports ?status=)
GET      /admin/orders/<id>
POST     /admin/orders/<id>/status
```

## 12. Python Concepts Used
- **Variables & data types** — strings, floats, integers, booleans
- **Functions** — `get_cart()`, `get_cart_details()`, `generate_order_number()`, etc.
- **Conditional statements** — validating form input, checking login state
- **Loops** — iterating over cart items, sample data insertion
- **Lists & dictionaries** — `ORDER_STATUSES`, `MENU_CATEGORIES`, cart dictionary, row objects
- **Exception handling** — `try/except` around type conversions and database writes
- **Database operations** — `sqlite3`, parameterized queries, CRUD (Create, Read, Update, Delete)
- **Flask routing** — `@app.route`, dynamic URL parameters, GET/POST methods
- **Sessions** — Flask `session` object for cart and admin login state
- **Decorators** — a custom `@login_required` decorator to protect admin routes

## 13. Future Improvements
- Password hashing for admin credentials (e.g., using `werkzeug.security`)
- Multiple admin accounts with role-based permissions
- Real-time order updates using WebSockets
- Payment gateway integration
- Customer accounts and order history
- Image upload instead of filename-based images
- Email/SMS order notifications

## 14. Viva Voce Questions and Answers

**Q1: What is Flask?**
A: Flask is a lightweight Python web framework used to build web applications. It's called a "micro-framework" because it provides the essentials (routing, templating, sessions) without forcing a specific project structure.

**Q2: What is SQLite and why was it used here?**
A: SQLite is a lightweight, file-based relational database that doesn't require a separate server process. It's ideal for small to medium projects like this one because the entire database lives in a single `.db` file.

**Q3: What is CRUD?**
A: CRUD stands for Create, Read, Update, Delete — the four basic operations performed on data. In CafeHub, the admin menu management feature demonstrates all four: adding items (Create), viewing items (Read), editing items (Update), and deleting items (Delete).

**Q4: What are Flask sessions and how are they used in this project?**
A: Sessions let the server remember information about a specific visitor across multiple requests, using a signed cookie stored in the browser. CafeHub uses sessions to store the shopping cart (so each visitor has their own cart) and to track whether the admin is logged in.

**Q5: What is Jinja2?**
A: Jinja2 is Flask's default templating engine. It allows Python-like expressions (loops, conditionals, variables) to be embedded inside HTML using `{% %}` and `{{ }}` syntax, so the same HTML template can render dynamic data.

**Q6: What is the difference between GET and POST?**
A: GET requests retrieve data and are typically used for viewing pages (parameters are visible in the URL). POST requests send data to the server, usually to create or update something (e.g., submitting the checkout form), and the data is sent in the request body instead of the URL.

**Q7: What are Python functions and why are they useful?**
A: A function is a reusable block of code that performs a specific task. In CafeHub, functions like `get_cart_details()` and `generate_order_number()` avoid repeating logic and make the code easier to read, test, and maintain.

**Q8: What are database tables and how are they related in this project?**
A: A table stores structured data in rows and columns. CafeHub has three tables: `menu_items`, `orders`, and `order_items`. `order_items` is related to both `orders` and `menu_items` through foreign keys, forming a one-to-many relationship (one order can have many order items).

**Q9: What is a primary key?**
A: A primary key is a column (usually `id`) that uniquely identifies each row in a table. In CafeHub, every table uses an auto-incrementing integer `id` as its primary key.

**Q10: What is a foreign key?**
A: A foreign key is a column that references the primary key of another table, used to link related data. In CafeHub, `order_items.order_id` references `orders.id`, and `order_items.menu_item_id` references `menu_items.id`.

**Q11: What is web application architecture, and how does this project follow it?**
A: Web application architecture describes how the frontend, backend, and database interact. CafeHub follows a simple three-tier structure: the **frontend** (HTML/CSS/JS templates) handles what the user sees, the **backend** (Flask/Python) handles logic and routing, and the **database** (SQLite) stores persistent data. The backend acts as the bridge between the frontend and the database.

**Q12: How does the shopping cart work without user accounts?**
A: The cart is stored as a dictionary inside the Flask session, which is tied to a signed cookie in the visitor's browser. This means each visitor gets their own cart without needing to log in or create an account.

**Q13: How is the admin panel protected?**
A: A custom Python decorator called `login_required` wraps every admin route. Before running the route's code, it checks whether `session['admin_logged_in']` is set to `True`; if not, it redirects the user to the login page.

**Q14: Why are parameterized queries used instead of directly inserting values into SQL strings?**
A: Parameterized queries (using `?` placeholders) prevent SQL injection attacks by treating user input strictly as data, never as executable SQL code.

**Q15: How does the application prevent duplicate sample data on every restart?**
A: The `init_db()` function checks `SELECT COUNT(*) FROM menu_items` before inserting sample data. If the table already has rows, it skips the insertion step.

---
Built as a Python/Flask college mini-project. Happy demoing! ☕
