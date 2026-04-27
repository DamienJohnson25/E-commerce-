"""
app.py — The Main Backend Server
==================================
This is the "brain" of our backend. It receives HTTP requests
from the Vue.js frontend, processes them, and sends back JSON responses.

Analogy: This is the HEAD CHEF who receives orders (requests),
delegates work to the kitchen staff (models.py), and sends
dishes (responses) back to the waiter (frontend).

To run: python app.py
Server starts at http://localhost:5000
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import (
    init_db, get_all_products, get_product_by_id, search_products,
    get_categories, add_to_cart, get_cart, update_cart_item,
    remove_from_cart, create_order, get_order,
    register_user, login_user, get_user_by_id
)
from email_service import send_order_confirmation, send_welcome_email

# ─── App Setup ─────────────────────────────────────────────────────
app = Flask(__name__)
# app.secret_key = 'shopvue-dev-secret-key-change-in-production'

# CORS: Allow the Vue.js frontend (port 5173) to talk to us
# supports_credentials=True allows cookies (session) to be sent cross-origin
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize the database tables on startup
init_db()


# ─── Health Check ──────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health_check():
    """A simple endpoint to verify the server is running.
    Like knocking on the restaurant door to see if they're open."""
    return jsonify({"status": "ok", "message": "ShopVue API is running!"})


# ─── Auth Endpoints ────────────────────────────────────────────────

@app.route('/api/auth/register', methods=['POST'])
def register():
    """POST /api/auth/register — Body: {name, email, password}
    Create a new user account.
    Like filling out a membership form at a club."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    # Validate inputs
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email or '@' not in email:
        return jsonify({"error": "A valid email is required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user = register_user(name, email, password)
    if not user:
        return jsonify({"error": "An account with this email already exists"}), 409

    # Store user id in the server-side session (the wristband)
    session['user_id'] = user['id']

    # Send welcome email (non-blocking — doesn't fail registration)
    send_welcome_email(user['name'], user['email'])

    return jsonify({"message": "Account created", "user": user}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """POST /api/auth/login — Body: {email, password}
    Log in to an existing account.
    Like showing your membership card at the door."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = login_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Store user id in session
    session['user_id'] = user['id']

    return jsonify({"message": "Login successful", "user": user})


@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """GET /api/auth/me
    Check who is currently logged in.
    Like asking: 'Whose wristband is this?'"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"user": None})

    user = get_user_by_id(user_id)
    return jsonify({"user": user})


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """POST /api/auth/logout
    Log out the current user.
    Like cutting off the wristband when leaving the club."""
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"})


# ─── Product Endpoints ─────────────────────────────────────────────

@app.route('/api/products', methods=['GET'])
def list_products():
    """GET /api/products?category=Electronics
    Returns all products, optionally filtered by category.
    Like asking: 'Show me the menu' or 'Show me just the desserts.'"""
    category = request.args.get('category', None)
    products = get_all_products(category)
    return jsonify(products)


@app.route('/api/products/search', methods=['GET'])
def search():
    """GET /api/products/search?q=headphones
    Search products by name or description.
    Like asking: 'Do you have anything with chocolate?'"""
    query = request.args.get('q', '')
    if not query or len(query.strip()) == 0:
        return jsonify([])
    results = search_products(query.strip())
    return jsonify(results)


@app.route('/api/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    """GET /api/products/5
    Get full details for a single product.
    Like asking: 'Tell me more about the salmon dish.'"""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route('/api/categories', methods=['GET'])
def list_categories():
    """GET /api/categories
    Returns all unique product categories.
    Like asking: 'What sections does your menu have?'"""
    categories = get_categories()
    return jsonify(categories)


# ─── Cart Endpoints ────────────────────────────────────────────────

@app.route('/api/cart', methods=['POST'])
def add_item_to_cart():
    """POST /api/cart — Body: {session_id, product_id, quantity}
    Add a product to the shopping cart.
    Like telling the waiter: 'I'll have two of the salmon.'"""
    data = request.get_json()

    # Validate input — make sure the order makes sense
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    session_id = data.get('session_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not session_id or not product_id:
        return jsonify({"error": "session_id and product_id are required"}), 400

    if quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400

    # Check if the product exists
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check stock
    if product['stock'] < quantity:
        return jsonify({"error": "Not enough stock available"}), 400

    add_to_cart(session_id, product_id, quantity)
    return jsonify({"message": "Item added to cart", "success": True}), 201


@app.route('/api/cart/<session_id>', methods=['GET'])
def view_cart(session_id):
    """GET /api/cart/abc-123
    View all items in a session's cart.
    Like asking: 'What have I ordered so far?'"""
    items = get_cart(session_id)
    total = sum(item['price'] * item['quantity'] for item in items)
    return jsonify({
        "items": items,
        "total": round(total, 2),
        "item_count": sum(item['quantity'] for item in items)
    })


@app.route('/api/cart/<int:item_id>', methods=['PUT'])
def update_cart(item_id):
    """PUT /api/cart/1 — Body: {quantity}
    Update the quantity of a cart item.
    Like saying: 'Actually, make that three salmons instead of two.'"""
    data = request.get_json()
    quantity = data.get('quantity', 1)
    update_cart_item(item_id, quantity)
    return jsonify({"message": "Cart updated", "success": True})


@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def delete_from_cart(item_id):
    """DELETE /api/cart/1
    Remove an item from the cart.
    Like saying: 'Cancel the appetizer.'"""
    remove_from_cart(item_id)
    return jsonify({"message": "Item removed", "success": True})


# ─── Order Endpoints ───────────────────────────────────────────────

@app.route('/api/orders', methods=['POST'])
def place_order():
    """POST /api/orders — Body: {session_id, customer_name, email, address, city, zip}
    Create an order from the current cart.
    Like saying: 'Check, please!' — finalizes everything."""
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
    """GET /api/orders/1
    Get the details of a completed order.
    Like asking: 'Can I see my receipt?'"""
    order = get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)


# ─── Error Handlers ────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ─── Start the Server ─────────────────────────────────────────────

if __name__ == '__main__':
    print("🚀 ShopVue API starting on http://localhost:5000")
    print("📖 Try visiting: http://localhost:5000/api/health")
    app.run(debug=True, port=5000)

