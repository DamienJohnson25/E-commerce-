"""
app.py — The Main Backend Server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from models import (
    init_db, get_all_products, get_product_by_id, search_products,
    get_categories, add_to_cart, get_cart, update_cart_item,
    remove_from_cart, create_order, get_order
)

# ─── App Setup ─────────────────────────────────────────────────────
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

init_db()

# ─── Stripe Setup ──────────────────────────────────────────────────
import os
import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# ─── Health Check ──────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "ShopVue API is running!"})

# ─── Product Endpoints ─────────────────────────────────────────────
@app.route('/api/products', methods=['GET'])
def list_products():
    category = request.args.get('category', None)
    products = get_all_products(category)
    return jsonify(products)

# ✅ UPDATED SEARCH (ADVANCED FILTERS)
@app.route('/api/products/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    try:
        min_price = float(min_price) if min_price else None
        max_price = float(max_price) if max_price else None
    except ValueError:
        return jsonify({"error": "Invalid price format"}), 400

    results = search_products(query, category, min_price, max_price)
    return jsonify(results)

@app.route('/api/debug/products', methods=['GET'])
def debug_products():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM products")
    data = cursor.fetchall()

    conn.close()
    return jsonify([row["name"] for row in data])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

# ─── Recommendations Endpoint ───────────────────────────────
@app.route('/api/products/<int:product_id>/recommendations', methods=['GET'])
def get_recommendations(product_id):
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT category FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product:
        conn.close()
        return jsonify([])
    category = product["category"]
    cursor.execute("""
        SELECT * FROM products
        WHERE category = ?
        AND id != ?
        ORDER BY rating DESC
        LIMIT 4
    """, (category, product_id))
    recommendations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(recommendations)

@app.route('/api/categories', methods=['GET'])
def list_categories():
    categories = get_categories()
    return jsonify(categories)

# ─── Authentication Endpoints ─────────────────────────────────────
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()

        user_id = cursor.lastrowid  # ✅ ADDED

        return jsonify({
            "id": user_id,  # ✅ ADDED
            "name": name,
            "email": email
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({
        "id": user[0],
        "name": user[1],
        "email": user[2]
    }), 200

# ✅ NEW DELETE ACCOUNT
@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully"}), 200

# ─── Cart Endpoints ────────────────────────────────────────────────
@app.route('/api/cart', methods=['POST'])
def add_item_to_cart():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    session_id = data.get('session_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not session_id or not product_id:
        return jsonify({"error": "session_id and product_id are required"}), 400
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    add_to_cart(session_id, product_id, quantity)
    return jsonify({"message": "Item added to cart", "success": True}), 201

@app.route('/api/cart/<session_id>', methods=['GET'])
def view_cart(session_id):
    items = get_cart(session_id)
    total = sum(item['price'] * item['quantity'] for item in items)
    return jsonify({
        "items": items,
        "total": round(total, 2),
        "item_count": sum(item['quantity'] for item in items)
    })

@app.route('/api/cart/<int:item_id>', methods=['PUT'])
def update_cart(item_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)
    update_cart_item(item_id, quantity)
    return jsonify({"message": "Cart updated", "success": True})

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def delete_from_cart(item_id):
    remove_from_cart(item_id)
    return jsonify({"message": "Item removed", "success": True})

# ─── Stripe Checkout Endpoint ───────────────────────────────────────
@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    items = data.get('items', [])

    if not items or len(items) == 0:
        return {"error": "Cart is empty"}, 400

    line_items = [
        {
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": item["name"],
                },
                "unit_amount": int(item["price"] * 100),
            },
            "quantity": item["quantity"],
        }
        for item in items
    ]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url="http://localhost:5173/checkout-success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:5173/cart",
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}, 500

# ─── Order Endpoints ───────────────────────────────────────────────
@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    required_fields = ['session_id', 'customer_name', 'customer_email', 'address', 'city', 'zip_code']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    order_id = create_order(**data)
    order = get_order(order_id)
    return jsonify(order), 201

# ─── Start the Server ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    