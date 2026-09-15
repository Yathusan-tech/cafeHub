# ☕ CafeHub

> A modern, responsive café management and online ordering web application built with Flask.

CafeHub is a full-stack café web application designed to provide customers with a smooth online browsing and ordering experience while giving administrators a dedicated management portal for handling menu items and orders.

The project focuses on a clean café-themed interface, reliable backend functionality, database-driven operations, responsive design, and secure administration.

---

## ✨ Features

### 👥 Customer Features

- 🏠 Modern café homepage
- 📖 Browse the complete menu
- 🔎 View menu items and details
- 🛒 Add items to cart
- 🧾 Review cart before checkout
- 💳 Checkout and order placement
- 📦 Order confirmation
- 📱 Responsive design for mobile, tablet, laptop and desktop
- 📍 Café contact and location information
- 🎨 Consistent café-themed user interface

### 🔐 Admin Features

CafeHub includes a dedicated administration area for authorized staff.

- 🔑 Secure admin login
- 📊 Dashboard overview
- 🍰 Add menu items
- ✏️ Edit menu items
- 🗑️ Delete menu items
- 🔄 Enable/disable menu availability
- 📦 View customer orders
- 🔄 Update order status
- ⚙️ Manage application settings
- 🔒 Protected administrative routes

The administration portal is intentionally separated from the customer-facing navigation.

---

## 🛠️ Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Responsive Web Design
- Poppins typography
- Custom café-themed UI

### Backend

- Python
- Flask
- Jinja2 Templates

### Database

- SQLite

### Production

- Gunicorn
- Render

### Development Tools

- Visual Studio Code
- Git
- GitHub
- GitHub Desktop
- PowerShell

---

## 🏗️ Project Architecture

```text
CafeHub/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── CafeHub/
│   ├── app.py
│   ├── database.db
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── menu.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   └── ...
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
└── ...

The exact structure may vary depending on the deployment configuration.

🚀 Getting Started
1. Clone the repository
git clone https://github.com/Yathusan-tech/cafeHub.git
2. Open the project
cd cafeHub
3. Create a virtual environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1

If PowerShell blocks script execution, use:

.venv\Scripts\python.exe -m pip install -r requirements.txt
4. Install dependencies
pip install -r requirements.txt
5. Run the application
python app.py

The application should be available at:

http://127.0.0.1:5000
🌐 Production Deployment

CafeHub can be deployed as a Python web service using Gunicorn.

Build Command
pip install -r requirements.txt
Start Command
gunicorn app:app

The application is configured to use the deployment environment's port when required.

🔐 Security

CafeHub is designed with several basic security considerations:

Password hashing for administrator credentials
Protected administrative routes
Session-based authentication
Environment-based configuration
No hard-coded production secrets
Input validation
Database-backed operations
Separation between customer and administrator functionality
Environment Variables

Production credentials and secrets should be provided through environment variables rather than committed to GitHub.

Example:

SECRET_KEY=your-secret-key
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-admin-password
PORT=5000

Never commit real credentials, API keys, or .env files to a public repository.

📱 Responsive Design

CafeHub is designed to provide a consistent experience across different screen sizes.

The interface is intended to support:

Mobile
├── 320px
├── 360px
├── 375px
├── 390px
├── 414px
└── 430px

Tablet
├── 600px
├── 768px
├── 820px
└── 1024px

Desktop
├── 1280px
├── 1366px
├── 1440px
├── 1600px
└── 1920px+

Large Displays
├── 2560px
└── 3840px

The goal is to maintain usable layouts, readable typography, properly sized images, accessible controls, and consistent spacing across devices.

🗄️ Database

CafeHub uses SQLite for application data during development.

The database handles application information such as:

Menu items
Customer orders
Order status
Administrator information
Application settings

Database initialization is designed to be safe and repeatable.

For production environments, persistent database storage should be configured appropriately because local SQLite storage on ephemeral hosting environments may not persist between service restarts or deployments.

🧪 Testing & Verification

Before deployment, the application should be verified across the major customer and administrator workflows.

Customer Flow
Homepage
   ↓
Menu
   ↓
Select Item
   ↓
Add to Cart
   ↓
Review Cart
   ↓
Checkout
   ↓
Place Order
   ↓
Order Confirmation
Admin Flow
Admin Login
   ↓
Dashboard
   ↓
Manage Menu
   ↓
Manage Orders
   ↓
Update Order Status

Testing should include:

Page loading
Navigation
Menu operations
Cart operations
Checkout
Order creation
Database operations
Admin authentication
Admin CRUD operations
Responsive layouts
Invalid input handling
Error pages
Production startup with Gunicorn
🎨 Design Philosophy

CafeHub follows a warm café-inspired visual identity.

The interface uses a combination of:

Warm coffee tones
Cream backgrounds
Brown accents
Gold highlights
Clean typography
Rounded cards
Responsive layouts
Professional spacing
Café-focused imagery

The goal is to provide a welcoming digital café experience without sacrificing usability.

📂 Main Application Components
Component	Purpose
app.py	Flask application entry point
templates/	HTML/Jinja templates
static/css/	Website styling
static/js/	Client-side functionality
static/images/	Website imagery
database.db	SQLite application database
requirements.txt	Python dependencies
.gitignore	Files excluded from Git
🔄 Application Flow
                ┌──────────────────┐
                │     Customer     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Flask Web App   │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │   Customer  │       │    Admin    │
       │   Features  │       │    Portal   │
       └──────┬──────┘       └──────┬──────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                ┌──────────────────┐
                │  SQLite Database │
                └──────────────────┘
📌 Project Goals

CafeHub aims to demonstrate the development of a complete web application using Python and Flask while maintaining:

Clean architecture
Reliable backend functionality
Database integration
Responsive frontend design
Secure administration
Maintainable code
Production deployment capability
User-friendly interaction
🚧 Future Improvements

Potential future enhancements include:

Online payment gateway integration
Customer accounts
Order history
Email/SMS order notifications
Advanced analytics dashboard
Inventory management
Table reservation
Persistent production database
Cloud image storage
Progressive Web App support
Advanced role-based administration
👨‍💻 Author

Yathusan

Computer Science & Engineering Student

GitHub:
https://github.com/Yathusan-tech

📄 License

This project is available for educational and development purposes.

If you intend to reuse, modify, or redistribute the project, please check the repository's licensing terms before doing so.

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

CafeHub — Bringing the café experience online. ☕


### One important thing before you make the repo public

Because your repository will become **public**, I would **not** put the real `database.db` or real admin credentials into GitHub.

Your `.gitignore` should ideally contain at least:

gitignore
.venv/
__pycache__/
*.pyc
.env
*.db
instance/
.vscode/
