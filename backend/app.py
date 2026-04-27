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

from email_service import send_order_confirmation, send_welcome_email
 
# ─── App Setup ─────────────────────────────────────────────────────
app = Flask(__name__)
 
CORS(app, resources={r"/api/*": {"origins": "*"}})
 
init_db()
 
 
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
 
 
@app.route('/api/products/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query or len(query.strip()) == 0:
        return jsonify([])
    results = search_products(query.strip())
    return jsonify(results)
 
 
@app.route('/api/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)
 
 
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
 
        # Send welcome email (non-blocking — doesn't fail registration)
        send_welcome_email(name, email)
 
        return jsonify({
            "name": name,
            "email": email,
            "message": "User registered successfully"
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
 
 
# ─── DELETE ACCOUNT ENDPOINT ───────────────────────────────────────
@app.route('/api/delete-account', methods=['DELETE'])
def delete_account():
    data = request.get_json()
 
    if not data:
        return jsonify({"error": "Request body is required"}), 400
 
    email = data.get('email')
 
    if not email:
        return jsonify({"error": "Email is required"}), 400
 
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
 
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
 
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
 
        return jsonify({"message": "Account deleted successfully"}), 200
 
    except Exception as e:
        print("Delete error:", e)
        return jsonify({"error": "Database error"}), 500
 
    finally:
        conn.close()
 
 
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
 
    if quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400
 
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
 
    if product['stock'] < quantity:
        return jsonify({"error": "Not enough stock available"}), 400
 
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
 
 
# ─── Order Endpoints ───────────────────────────────────────────────
@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
 
    if not data:
        return jsonify({"error": "Request body is required"}), 400
 
    required_fields = ['session_id', 'customer_name', 'customer_email', 'address', 'city', 'zip_code']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
 
    order_id = create_order(
        session_id=data['session_id'],
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        address=data['address'],
        city=data['city'],
        zip_code=data['zip_code']
    )
 
    if not order_id:
        return jsonify({"error": "Cart is empty — nothing to order"}), 400
 
    order = get_order(order_id)
 
    # Send order confirmation email (non-blocking — doesn't fail the order)
    send_order_confirmation(order)
 
    return jsonify(order), 201
 
 
@app.route('/api/orders/<int:order_id>', methods=['GET'])
def order_detail(order_id):
    order = get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)
 
@app.route('/api/debug-env', methods=['GET'])
def debug_env():
    import os
    return jsonify({
        "SMTP_USER": os.environ.get('SMTP_USER', 'NOT SET'),
        "SMTP_KEY": "SET" if os.environ.get('SMTP_KEY') else "NOT SET",
        "SENDER_EMAIL": os.environ.get('SENDER_EMAIL', 'NOT SET'),
    })
 
# ─── Error Handlers ────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404
 
 
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500
 

# ─── Start the Server ─────────────────────────────────────────────
if __name__ == '__main__':
    print("ShopVue API starting on http://localhost:5000")
    print("Try visiting: http://localhost:5000/api/health")
    app.run(debug=True, port=5000)