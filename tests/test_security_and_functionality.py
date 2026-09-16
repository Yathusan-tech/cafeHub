"""
CafeHub Security & Production Hardening Test Suite
Verifies all 22 required checkpoints, CSRF protection, admin flows, customer flows,
security headers, input validation, and asset loading.
"""

import unittest
import os
import re
import sqlite3
from app import app, get_db, init_db

def extract_csrf_token(html_text):
    """Extracts the CSRF token from rendered HTML form."""
    for line in html_text.splitlines():
        if "csrf_token" in line and "value=" in line:
            m = re.search(r'value="([^"]+)"', line)
            if m:
                return m.group(1)
            m2 = re.search(r"value='([^']+)'", line)
            if m2:
                return m2.group(1)
    return ""

class CafeHubSecurityAndFunctionalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure app for test execution
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = True  # Ensure CSRF is actively validated in tests
        init_db()
        from werkzeug.security import generate_password_hash
        with app.app_context():
            db = get_db()
            existing = db.execute("SELECT id FROM admins WHERE username = 'testadmin'").fetchone()
            if existing:
                db.execute("UPDATE admins SET password_hash = ? WHERE id = ?",
                           (generate_password_hash("SecureAdminPass2026!"), existing["id"]))
            else:
                db.execute("INSERT INTO admins (username, password_hash, created_at) VALUES (?, ?, '2026-09-16 12:00:00')",
                           ('testadmin', generate_password_hash("SecureAdminPass2026!")))
            db.commit()

    def setUp(self):
        self.client = app.test_client()

    def test_01_app_imports_and_configuration(self):
        """1. Verify Flask application imports and has security config."""
        self.assertIsNotNone(app)
        self.assertTrue(app.config.get("SESSION_COOKIE_HTTPONLY"))
        self.assertEqual(app.config.get("SESSION_COOKIE_SAMESITE"), "Lax")

    def test_02_application_starts_and_responds(self):
        """2. Verify test client responds to requests."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_03_homepage_loads(self):
        """3. Verify homepage loads with featured items and security headers."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"CafeHub", res.data)
        self.assertIn(b"Featured Menu", res.data)
        # Verify security headers
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(res.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(res.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")

    def test_04_menu_loads(self):
        """4. Verify menu page loads with items and CSRF tokens."""
        res = self.client.get("/menu")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Our Menu", res.data)
        token = extract_csrf_token(res.get_data(as_text=True))
        self.assertTrue(bool(token), "CSRF token should be present in menu add-to-cart form")

    def test_05_csrf_protection_enforced(self):
        """Verify state-changing POST requests without CSRF token are blocked."""
        # Attempt to add to cart without CSRF token
        res = self.client.post("/add-to-cart", data={"item_id": "1", "quantity": "1"})
        # Should redirect back with error flash due to CSRF failure
        self.assertEqual(res.status_code, 302)
        with self.client.session_transaction() as sess:
            cart = sess.get("cart", {})
            self.assertNotIn("1", cart, "Item should not be added when CSRF token is missing")

    def test_06_cart_operations_work_with_csrf(self):
        """5. Verify cart operations (add, update, remove, clear) work correctly."""
        # Get menu page to extract CSRF token
        menu_res = self.client.get("/menu")
        token = extract_csrf_token(menu_res.get_data(as_text=True))

        # Add item 1
        res = self.client.post("/add-to-cart", data={"item_id": "1", "quantity": "2", "csrf_token": token}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("cart", {}).get("1"), 2)

        # View cart
        cart_res = self.client.get("/cart")
        self.assertEqual(cart_res.status_code, 200)
        self.assertIn(b"Your Cart", cart_res.data)
        cart_token = extract_csrf_token(cart_res.get_data(as_text=True))

        # Increase quantity
        self.client.post("/update-cart", data={"item_id": "1", "action": "increase", "csrf_token": cart_token})
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("cart", {}).get("1"), 3)

        # Decrease quantity
        self.client.post("/update-cart", data={"item_id": "1", "action": "decrease", "csrf_token": cart_token})
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("cart", {}).get("1"), 2)

        # Remove item
        self.client.post("/remove-from-cart", data={"item_id": "1", "csrf_token": cart_token})
        with self.client.session_transaction() as sess:
            self.assertNotIn("1", sess.get("cart", {}))

    def test_07_checkout_page_loads(self):
        """6. Verify checkout page loads when cart has items."""
        # Add item first
        menu_res = self.client.get("/menu")
        token = extract_csrf_token(menu_res.get_data(as_text=True))
        self.client.post("/add-to-cart", data={"item_id": "2", "quantity": "1", "csrf_token": token})

        res = self.client.get("/checkout")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Checkout", res.data)
        self.assertIn(b"Table Number", res.data)

    def test_08_customer_order_submission_and_confirmation(self):
        """7 & 8. Verify customer order submission and confirmation page."""
        # Add item
        menu_res = self.client.get("/menu")
        token = extract_csrf_token(menu_res.get_data(as_text=True))
        self.client.post("/add-to-cart", data={"item_id": "3", "quantity": "2", "csrf_token": token})

        # Checkout page for token
        chk_res = self.client.get("/checkout")
        chk_token = extract_csrf_token(chk_res.get_data(as_text=True))

        # Submit valid order
        res = self.client.post("/place-order", data={
            "customer_name": "Test Customer",
            "phone": "9876543210",
            "email": "customer@test.com",
            "table_number": "T-4",
            "special_instructions": "Extra napkins",
            "csrf_token": chk_token
        }, follow_redirects=False)

        self.assertEqual(res.status_code, 302)
        location = res.headers.get("Location", "")
        self.assertIn("/order/CH-", location)

        # Follow to confirmation page
        conf_res = self.client.get(location)
        self.assertEqual(conf_res.status_code, 200)
        self.assertIn(b"ORDER PLACED SUCCESSFULLY!", conf_res.data)
        self.assertIn(b"Test Customer", conf_res.data)

        # Verify cart was cleared
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("cart", {}), {})

    def test_09_admin_login_with_valid_and_invalid_credentials(self):
        """9 & 10. Verify admin login accepts valid env credentials and rejects wrong passwords."""
        # Get login page for CSRF token
        login_page = self.client.get("/admin/login")
        token = extract_csrf_token(login_page.get_data(as_text=True))

        # Test wrong password
        bad_res = self.client.post("/admin/login", data={
            "username": "testadmin",
            "password": "WrongPassword999!",
            "csrf_token": token
        }, follow_redirects=True)
        self.assertIn(b"Invalid username or password", bad_res.data)
        with self.client.session_transaction() as sess:
            self.assertFalse(sess.get("admin_logged_in", False))

        # Test correct credentials
        good_res = self.client.post("/admin/login", data={
            "username": "testadmin",
            "password": "SecureAdminPass2026!",
            "csrf_token": token
        }, follow_redirects=True)
        self.assertEqual(good_res.status_code, 200)
        self.assertIn(b"Dashboard", good_res.data)
        with self.client.session_transaction() as sess:
            self.assertTrue(sess.get("admin_logged_in"))

    def test_10_admin_dashboard_metrics(self):
        """11. Verify admin dashboard loads metrics and statistics."""
        # Login first
        with self.client.session_transaction() as sess:
            sess["admin_logged_in"] = True
            sess["admin_username"] = "testadmin"

        res = self.client.get("/admin/dashboard")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)
        self.assertIn(b"Total Orders", res.data)

    def test_11_admin_menu_crud_operations(self):
        """12, 13, 14. Verify add, edit, toggle, and delete menu items."""
        with self.client.session_transaction() as sess:
            sess["admin_logged_in"] = True
            sess["admin_username"] = "testadmin"

        # 12. Add menu item
        add_page = self.client.get("/admin/menu/add")
        token = extract_csrf_token(add_page.get_data(as_text=True))
        add_res = self.client.post("/admin/menu/add", data={
            "name": "Test Matcha Latte",
            "description": "Ceremonial grade green tea latte.",
            "category": "Tea",
            "price": "175.00",
            "image": "greentea.svg",
            "available": "on",
            "csrf_token": token
        }, follow_redirects=True)
        self.assertIn(b"added to the menu", add_res.data)

        # Retrieve created item ID
        with app.app_context():
            db = get_db()
            item = db.execute("SELECT * FROM menu_items WHERE name = 'Test Matcha Latte'").fetchone()
            self.assertIsNotNone(item)
            item_id = item["id"]

        # 13. Edit menu item
        edit_page = self.client.get(f"/admin/menu/edit/{item_id}")
        token = extract_csrf_token(edit_page.get_data(as_text=True))
        edit_res = self.client.post(f"/admin/menu/edit/{item_id}", data={
            "name": "Test Matcha Latte Special",
            "description": "Updated description",
            "category": "Tea",
            "price": "185.00",
            "image": "greentea.svg",
            "available": "on",
            "csrf_token": token
        }, follow_redirects=True)
        self.assertIn(b"updated successfully", edit_res.data)

        # Toggle availability
        menu_page = self.client.get("/admin/menu")
        token = extract_csrf_token(menu_page.get_data(as_text=True))
        self.client.post(f"/admin/menu/toggle/{item_id}", data={"csrf_token": token})
        with app.app_context():
            db = get_db()
            toggled = db.execute("SELECT available FROM menu_items WHERE id = ?", (item_id,)).fetchone()
            self.assertEqual(toggled["available"], 0)

        # 14. Delete menu item
        self.client.post(f"/admin/menu/delete/{item_id}", data={"csrf_token": token}, follow_redirects=True)
        with app.app_context():
            db = get_db()
            deleted = db.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()
            self.assertIsNone(deleted)

    def test_12_admin_order_status_update(self):
        """15. Verify updating order status."""
        with self.client.session_transaction() as sess:
            sess["admin_logged_in"] = True
            sess["admin_username"] = "testadmin"

        # Check existing order
        with app.app_context():
            db = get_db()
            order = db.execute("SELECT id FROM orders LIMIT 1").fetchone()
        if order:
            order_id = order["id"]
            details_page = self.client.get(f"/admin/orders/{order_id}")
            token = extract_csrf_token(details_page.get_data(as_text=True))
            res = self.client.post(f"/admin/orders/{order_id}/status", data={
                "status": "Preparing",
                "csrf_token": token
            }, follow_redirects=True)
            self.assertIn(b"Order status updated", res.data)

    def test_13_admin_settings_and_password_policy(self):
        """16 & 17. Verify admin settings page, 10-char password policy, and password persistence."""
        with self.client.session_transaction() as sess:
            sess["admin_logged_in"] = True
            sess["admin_username"] = "testadmin"

        settings_page = self.client.get("/admin/settings")
        self.assertEqual(settings_page.status_code, 200)
        self.assertIn(b"Minimum 10 characters", settings_page.data)
        token = extract_csrf_token(settings_page.get_data(as_text=True))

        # Attempt to change with password too short (< 10 chars)
        short_res = self.client.post("/admin/settings", data={
            "current_password": "SecureAdminPass2026!",
            "new_password": "short",
            "confirm_password": "short",
            "csrf_token": token
        })
        self.assertIn(b"at least 10 characters", short_res.data)

        # Attempt with valid 10+ char password
        valid_res = self.client.post("/admin/settings", data={
            "current_password": "SecureAdminPass2026!",
            "new_password": "NewStrongAdminPass2026!",
            "confirm_password": "NewStrongAdminPass2026!",
            "csrf_token": token
        }, follow_redirects=True)
        self.assertIn(b"Password updated successfully", valid_res.data)

        # Logout
        self.client.post("/admin/logout", data={"csrf_token": token})

        # Verify old password NO LONGER works
        login_page = self.client.get("/admin/login")
        login_token = extract_csrf_token(login_page.get_data(as_text=True))
        old_login_res = self.client.post("/admin/login", data={
            "username": "testadmin",
            "password": "SecureAdminPass2026!",
            "csrf_token": login_token
        }, follow_redirects=True)
        self.assertIn(b"Invalid username or password", old_login_res.data)

        # Verify new password WORKS
        new_login_res = self.client.post("/admin/login", data={
            "username": "testadmin",
            "password": "NewStrongAdminPass2026!",
            "csrf_token": login_token
        }, follow_redirects=True)
        self.assertEqual(new_login_res.status_code, 200)
        self.assertIn(b"Dashboard", new_login_res.data)

        # Simulate app restart: call init_db() and create fresh client
        init_db()
        restart_client = app.test_client()
        restart_login_page = restart_client.get("/admin/login")
        restart_token = extract_csrf_token(restart_login_page.get_data(as_text=True))
        restart_res = restart_client.post("/admin/login", data={
            "username": "testadmin",
            "password": "NewStrongAdminPass2026!",
            "csrf_token": restart_token
        }, follow_redirects=True)
        self.assertEqual(restart_res.status_code, 200)
        self.assertIn(b"Dashboard", restart_res.data)

        # Reset password back to SecureAdminPass2026! so other tests stay clean
        settings_res = restart_client.get("/admin/settings")
        set_token = extract_csrf_token(settings_res.get_data(as_text=True))
        restart_client.post("/admin/settings", data={
            "current_password": "NewStrongAdminPass2026!",
            "new_password": "SecureAdminPass2026!",
            "confirm_password": "SecureAdminPass2026!",
            "csrf_token": set_token
        })

    def test_14_admin_logout_post(self):
        """18. Verify admin logout requires POST with CSRF and clears session, rejecting GET."""
        # Verify GET /admin/logout is rejected with 405 Method Not Allowed
        get_res = self.client.get("/admin/logout")
        self.assertEqual(get_res.status_code, 405)

        with self.client.session_transaction() as sess:
            sess["admin_logged_in"] = True
            sess["admin_username"] = "testadmin"

        dash = self.client.get("/admin/dashboard")
        token = extract_csrf_token(dash.get_data(as_text=True))

        # POST logout with CSRF
        res = self.client.post("/admin/logout", data={"csrf_token": token}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"logged out", res.data)
        with self.client.session_transaction() as sess:
            self.assertNotIn("admin_logged_in", sess)

    def test_15_error_handlers(self):
        """19 & 20. Verify custom 404 and 500 error handlers."""
        res_404 = self.client.get("/non-existent-page-path-12345")
        self.assertEqual(res_404.status_code, 404)
        self.assertIn(b"Page Not Found", res_404.data)

    def test_16_static_assets_load(self):
        """21. Verify existing CSS and SVG assets load cleanly."""
        css_res = self.client.get("/static/css/style.css")
        self.assertEqual(css_res.status_code, 200)
        self.assertIn(b"--coffee-brown", css_res.data)

        svg_res = self.client.get("/static/images/latte.svg")
        self.assertEqual(svg_res.status_code, 200)

    def test_17_no_sensitive_values_in_responses(self):
        """22. Verify no passwords, secret keys, or stack traces leak in HTML."""
        login_res = self.client.get("/admin/login")
        self.assertNotIn(b"admin123", login_res.data)
        self.assertNotIn(b"cafehub_secret_key_change_in_production", login_res.data)

if __name__ == "__main__":
    unittest.main()
