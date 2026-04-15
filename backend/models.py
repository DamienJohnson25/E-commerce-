"""
models.py — Database Table Definitions
========================================
Think of this file as the BLUEPRINT for our database tables.
Each class represents a table, and each method handles
creating, reading, updating, or deleting rows.

Analogy: This is like designing the spreadsheets before
entering any data — you decide column names and types first.
"""

import sqlite3
import os
from datetime import datetime
import bcrypt


DATABASE = os.path.join(os.path.dirname(__file__), 'shop.db')



def get_db():
    """Get a connection to the database.
    Think of this as 'opening the filing cabinet.'"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't exist.
    Think of this as 'setting up empty spreadsheets.'"""
    conn = get_db()
    cursor = conn.cursor()

    # Products table — our inventory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT DEFAULT '',
            category TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            featured INTEGER DEFAULT 0,
            rating REAL DEFAULT 4.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Cart items table — what shoppers are considering
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Orders table — completed purchases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Order items — line items in each order
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    conn.commit()
    conn.close()


# ─── Product Operations ──────────────────────────────────────────

def get_all_products(category=None):
    """Fetch all products, optionally filtered by category."""
    conn = get_db()
    if category and category != 'all':
        rows = conn.execute(
            'SELECT * FROM products WHERE category = ? ORDER BY featured DESC, id',
            (category,)
        ).fetchall()
    else:
        rows = conn.execute(
            'SELECT * FROM products ORDER BY featured DESC, id'
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_product_by_id(product_id):
    """Fetch a single product by its ID."""
    conn = get_db()
    row = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def search_products(query='', category=None, min_price=None, max_price=None):
    conn = get_db()

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    # 🔍 Search text
    if query:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
        q = f"%{query.lower()}%"
        params.extend([q, q])

    # 📦 Category filter
    if category and category != 'all':
        sql += " AND category = ?"
        params.append(category)

    # 💰 Price filters
    if min_price:
        sql += " AND price >= ?"
        params.append(min_price)

    if max_price:
        sql += " AND price <= ?"
        params.append(max_price)

    # ⭐ Optional: sorting (later)
    sql += " ORDER BY featured DESC, id"

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in rows]


def get_categories():
    """Get all unique categories."""
    conn = get_db()
    rows = conn.execute('SELECT DISTINCT category FROM products ORDER BY category').fetchall()
    conn.close()
    return [row['category'] for row in rows]


# ─── Cart Operations ──────────────────────────────────────────────

def add_to_cart(session_id, product_id, quantity=1):
    """Add a product to the cart. If it already exists, increase quantity."""
    conn = get_db()

    # Check if item already in cart
    existing = conn.execute(
        'SELECT * FROM cart_items WHERE session_id = ? AND product_id = ?',
        (session_id, product_id)
    ).fetchone()

    if existing:
        new_qty = existing['quantity'] + quantity
        conn.execute(
            'UPDATE cart_items SET quantity = ? WHERE id = ?',
            (new_qty, existing['id'])
        )
    else:
        conn.execute(
            'INSERT INTO cart_items (session_id, product_id, quantity) VALUES (?, ?, ?)',
            (session_id, product_id, quantity)
        )

    conn.commit()
    conn.close()
    return True


def get_cart(session_id):
    """Get all cart items for a session, with product details."""
    conn = get_db()
    rows = conn.execute('''
        SELECT ci.id, ci.quantity, p.id as product_id, p.name, p.price,
               p.image_url, p.stock
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.session_id = ?
    ''', (session_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_cart_item(item_id, quantity):
    """Update the quantity of a cart item."""
    conn = get_db()
    if quantity <= 0:
        conn.execute('DELETE FROM cart_items WHERE id = ?', (item_id,))
    else:
        conn.execute('UPDATE cart_items SET quantity = ? WHERE id = ?', (quantity, item_id))
    conn.commit()
    conn.close()
    return True


def remove_from_cart(item_id):
    """Remove an item from the cart."""
    conn = get_db()
    conn.execute('DELETE FROM cart_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return True


def clear_cart(session_id):
    """Remove all items from a session's cart."""
    conn = get_db()
    conn.execute('DELETE FROM cart_items WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()
    return True


# ─── Order Operations ─────────────────────────────────────────────

def create_order(session_id, customer_name, customer_email, address, city, zip_code):
    """Create an order from the current cart contents."""
    conn = get_db()

    # Get cart items
    cart_items = get_cart(session_id)
    if not cart_items:
        conn.close()
        return None

    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    # Create the order
    cursor = conn.execute(
        '''INSERT INTO orders (session_id, customer_name, customer_email,
           address, city, zip_code, total) VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (session_id, customer_name, customer_email, address, city, zip_code, total)
    )
    order_id = cursor.lastrowid

    # Create order items
    for item in cart_items:
        conn.execute(
            '''INSERT INTO order_items (order_id, product_id, product_name, price, quantity)
               VALUES (?, ?, ?, ?, ?)''',
            (order_id, item['product_id'], item['name'], item['price'], item['quantity'])
        )

    # Update stock
    for item in cart_items:
        conn.execute(
            'UPDATE products SET stock = stock - ? WHERE id = ?',
            (item['quantity'], item['product_id'])
        )

    conn.commit()
    conn.close()

    # Clear the cart after ordering
    clear_cart(session_id)

    return order_id


def get_order(order_id):
    """Get order details with line items."""
    conn = get_db()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if not order:
        conn.close()
        return None

    items = conn.execute(
        'SELECT * FROM order_items WHERE order_id = ?', (order_id,)
    ).fetchall()

    conn.close()
    result = dict(order)
    result['items'] = [dict(i) for i in items]
    return result


def create_user(name, email, password):
    """Create a new user with hashed password."""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()
