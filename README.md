\# ☕ CafeHub



\### Modern Café Management \& Online Ordering Web Application



CafeHub is a full-stack café web application built with \*\*Python and Flask\*\*. It provides customers with a clean and responsive interface for exploring the café menu, managing their cart, placing orders, and receiving order confirmations.



The application also includes a dedicated \*\*administration portal\*\* for authorized staff to manage menu items, monitor customer orders, update order statuses, and manage application settings.



\---



\## ✨ Key Features



\### 👤 Customer Experience



\- 🏠 Café homepage

\- 📋 Browse complete menu

\- ☕ View food and beverage items

\- 🛒 Add items to cart

\- ➕ Increase or decrease quantities

\- 🗑️ Remove items from cart

\- 💰 Automatic order total calculation

\- 🧾 Checkout system

\- 📦 Place orders

\- ✅ Order confirmation

\- 📍 Café contact information

\- 📱 Responsive design

\- 🎨 Consistent café-themed visual design



\---



\### 🔐 Administration Portal



CafeHub includes a dedicated administration area that is separated from the customer-facing website.



Authorized administrators can:



\- 🔑 Securely log in

\- 📊 View dashboard information

\- ➕ Add menu items

\- ✏️ Edit menu items

\- 🗑️ Delete menu items

\- 🔄 Enable or disable menu availability

\- 📦 View customer orders

\- 🔄 Update order status

\- ⚙️ Manage application settings

\- 🔒 Access protected administrative routes

\- 🚪 Securely log out



The administration portal is intentionally kept separate from the main customer navigation.



\---



\## 🛠️ Technology Stack



\### Frontend



\- HTML5

\- CSS3

\- JavaScript

\- Jinja2 Templates

\- Responsive Web Design



\### Backend



\- Python

\- Flask

\- Gunicorn



\### Database



\- SQLite



\### Development \& Deployment



\- Git

\- GitHub

\- GitHub Desktop

\- Visual Studio Code

\- Command Prompt / PowerShell

\- Render



\---



\## 🏗️ Application Architecture



```text

&#x20;                        ┌──────────────────────┐

&#x20;                        │       CafeHub        │

&#x20;                        │   Web Application     │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;                   ┌───────────────┴───────────────┐

&#x20;                   │                               │

&#x20;                   ▼                               ▼

&#x20;         ┌──────────────────┐             ┌──────────────────┐

&#x20;         │ Customer Website │             │  Admin Portal    │

&#x20;         └────────┬─────────┘             └────────┬─────────┘

&#x20;                  │                                │

&#x20;                  └──────────────┬─────────────────┘

&#x20;                                 ▼

&#x20;                        ┌──────────────────┐

&#x20;                        │   Flask Backend  │

&#x20;                        └────────┬─────────┘

&#x20;                                 │

&#x20;                                 ▼

&#x20;                        ┌──────────────────┐

&#x20;                        │  SQLite Database │

&#x20;                        └──────────────────┘

````



\---



\## 📂 Project Structure



```text

CafeHub/

│

├── app.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── templates/

│   ├── base.html

│   ├── index.html

│   ├── menu.html

│   ├── cart.html

│   ├── checkout.html

│   └── ...

│

├── static/

│   ├── css/

│   ├── js/

│   └── images/

│

└── ...

```



> The exact structure may vary depending on the local and deployment configuration.



\---



\## 🚀 Getting Started



\### 1. Clone the Repository



```bash

git clone https://github.com/Yathusan-tech/cafeHub.git

```



\### 2. Navigate to the Project



```bash

cd cafeHub

```



\### 3. Create a Virtual Environment



```powershell

python -m venv .venv

```



\### 4. Activate the Virtual Environment



Windows:



```powershell

.venv\\Scripts\\activate

```



\### 5. Install Dependencies



```powershell

pip install -r requirements.txt

```



\### 6. Run the Application



```powershell

python app.py

```



\### 7. Open the Website



```text

http://127.0.0.1:5000

```



\---



\## 🛒 Customer Ordering Flow



```text

Homepage

&#x20;   │

&#x20;   ▼

Browse Menu

&#x20;   │

&#x20;   ▼

Select Items

&#x20;   │

&#x20;   ▼

Add to Cart

&#x20;   │

&#x20;   ▼

Review Cart

&#x20;   │

&#x20;   ▼

Checkout

&#x20;   │

&#x20;   ▼

Place Order

&#x20;   │

&#x20;   ▼

Order Confirmation

```



\---



\## 🔐 Administration Flow



```text

Admin Login

&#x20;    │

&#x20;    ▼

Admin Dashboard

&#x20;    │

&#x20;    ├──────────────► Manage Menu

&#x20;    │

&#x20;    ├──────────────► Manage Orders

&#x20;    │

&#x20;    └──────────────► Application Settings

```



Administrative functionality is protected through authentication and is intentionally separated from the public customer website.



\---



\## 📱 Responsive Design



CafeHub is designed to provide a consistent experience across different screen sizes.



\### Mobile



\* 320px

\* 360px

\* 375px

\* 390px

\* 414px

\* 430px



\### Tablet



\* 600px

\* 768px

\* 820px

\* 1024px



\### Desktop



\* 1280px

\* 1366px

\* 1440px

\* 1600px

\* 1920px



\### Large Displays



\* 2560px

\* 3840px



The responsive layout focuses on:



\* Readable typography

\* Proper spacing

\* Responsive navigation

\* Correct image sizing

\* Usable buttons

\* Flexible layouts

\* Mobile-friendly forms

\* Consistent cards

\* Appropriate content scaling



\---



\## 🎨 Design



CafeHub uses a warm café-inspired visual identity.



\### Design Characteristics



\* Coffee-inspired colors

\* Warm brown tones

\* Gold accents

\* Cream backgrounds

\* Clean typography

\* Café imagery

\* Structured content cards

\* Responsive layouts

\* Consistent buttons and components



The website maintains a consistent visual experience across customer pages and administrative functionality.



\---



\## 🗄️ Database



CafeHub uses \*\*SQLite\*\* for application data storage.



The database can contain information related to:



\* Menu items

\* Customer orders

\* Order status

\* Administrator information

\* Application settings



\### Production Consideration



SQLite is suitable for development and smaller applications.



For larger production workloads requiring:



\* Higher concurrency

\* Reliable persistence

\* Automated backups

\* Scalability



a managed database such as \*\*PostgreSQL\*\* is recommended.



\---



\## 🔒 Security



CafeHub incorporates several security-focused practices:



\* Protected administrative routes

\* Session-based authentication

\* Password hashing

\* Input validation

\* Environment-based configuration

\* Avoidance of hard-coded production secrets

\* Database-backed operations

\* Separation of customer and administrative functionality

\* Production configuration without debug mode



\### Environment Variables



Example:



```env

SECRET\_KEY=your-secret-key

ADMIN\_USERNAME=your-admin-username

ADMIN\_PASSWORD=your-admin-password

PORT=5000

```



> Never commit real passwords, API keys, secret keys, production credentials, or other sensitive information to GitHub.



\---



\## 🧪 Testing \& Verification



Important areas to verify before deployment include:



\### Customer



\* Homepage

\* Navigation

\* Menu

\* Item selection

\* Cart

\* Quantity changes

\* Item removal

\* Price calculations

\* Checkout

\* Order creation

\* Order confirmation

\* Contact information

\* Responsive layouts



\### Administration



\* Admin login

\* Authentication protection

\* Dashboard

\* Add menu item

\* Edit menu item

\* Delete menu item

\* Menu availability

\* Order management

\* Order status updates

\* Application settings

\* Logout



\### Production



\* Gunicorn startup

\* Flask application import

\* Environment variables

\* Debug mode disabled

\* Static files

\* Database initialization

\* Customer routes

\* Administrative routes



\---



\## 🌐 Deployment



CafeHub can be deployed using platforms such as \*\*Render\*\*.



\### Build Command



```bash

pip install -r requirements.txt

```



\### Start Command



```bash

gunicorn app:app

```



The application should use the hosting platform's provided port configuration.



\### Production Database



When deploying with SQLite, remember that some hosting environments may use ephemeral storage.



For a production application requiring persistent customer orders and data, use persistent storage or a managed database such as PostgreSQL.



\---



\## 🔄 Development Workflow



```text

Develop

&#x20;  │

&#x20;  ▼

Test Locally

&#x20;  │

&#x20;  ▼

Review Changes

&#x20;  │

&#x20;  ▼

Git Add

&#x20;  │

&#x20;  ▼

Git Commit

&#x20;  │

&#x20;  ▼

Git Push

&#x20;  │

&#x20;  ▼

GitHub

&#x20;  │

&#x20;  ▼

Deployment

```



\---



\## 📋 Git Commands



Check repository status:



```bash

git status

```



Stage changes:



```bash

git add .

```



Create a commit:



```bash

git commit -m "Describe your changes"

```



Push changes:



```bash

git push origin main

```



\---



\## 📈 Future Improvements



Possible future enhancements include:



\* 💳 Online payment integration

\* 👤 Customer accounts

\* 📦 Customer order history

\* 📧 Email notifications

\* 📱 SMS notifications

\* 📊 Advanced analytics

\* 📦 Inventory management

\* 🪑 Table reservation

\* 🗄️ PostgreSQL production database

\* ☁️ Cloud image storage

\* 🔔 Real-time notifications

\* 📱 Progressive Web App

\* 👥 Role-based access control

\* 💰 Sales and revenue reporting



\---



\## 🎯 Project Objectives



CafeHub demonstrates the development of a complete Python-based web application incorporating:



\* Frontend development

\* Backend development

\* Database integration

\* Authentication

\* CRUD operations

\* Business logic

\* Responsive web design

\* Security practices

\* Git and GitHub workflow

\* Production deployment



\---



\## 💡 Why CafeHub?



CafeHub combines a customer ordering experience with a dedicated management system.



```text

Frontend

&#x20;   +

Backend

&#x20;   +

Database

&#x20;   +

Authentication

&#x20;   +

Business Logic

&#x20;   +

Deployment

&#x20;   =

Complete Web Application

```



\---



\## 👨‍💻 Author



\### Yathusan



Computer Science \& Engineering Student



GitHub:



\[https://github.com/Yathusan-tech](https://github.com/Yathusan-tech)



\---



\## ⭐ Contributing



Contributions are welcome.



1\. Fork the repository

2\. Create a new branch

3\. Make your changes

4\. Test the application

5\. Commit your changes

6\. Push the branch

7\. Open a Pull Request



\---



\## 📄 License



CafeHub is currently intended for educational and development purposes.



If the project is reused, modified, or redistributed, appropriate licensing terms should be added.



\---



\## ☕ CafeHub



\### A digital café experience built with Python, Flask, and modern web technologies.



\*\*Browse. Order. Manage. Enjoy.\*\*



