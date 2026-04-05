"""
test_backend.py — Backend Tests
=================================
These tests verify that every API endpoint works correctly.

Analogy: This is the HEALTH INSPECTOR checking that:
- The kitchen produces correct dishes (correct responses)
- Bad orders are rejected (error handling)
- The inventory system works (cart & orders)

Run with: python -m pytest test_backend.py -v
"""

import sys
import os
import json
import pytest

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app
from models import init_db, get_db
from seed_data import seed


# ─── Test Setup ────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def setup_test_db():
    """Before each test, reset the database with seed data.
    Like cleaning the kitchen before each service."""
    seed()
    yield
    # Cleanup happens automatically via seed() next time


@pytest.fixture
def client():
    """Create a test client — a fake browser that sends requests.
    Like a food critic visiting the restaurant undercover."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ─── Health Check Tests ────────────────────────────────────────────

class TestHealthCheck:
    """Is the restaurant open?"""

    def test_health_endpoint_returns_200(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_ok_status(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert data['status'] == 'ok'


# ─── Product Tests ─────────────────────────────────────────────────

class TestProducts:
    """Can we see the menu?"""

    def test_list_all_products(self, client):
        """GET /api/products returns a list of products."""
        response = client.get('/api/products')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_products_have_required_fields(self, client):
        """Each product should have name, price, description, etc."""
        response = client.get('/api/products')
        data = response.get_json()
        product = data[0]
        required_fields = ['id', 'name', 'description', 'price', 'category', 'stock']
        for field in required_fields:
            assert field in product, f"Missing field: {field}"

    def test_filter_by_category(self, client):
        """GET /api/products?category=Electronics filters correctly."""
        response = client.get('/api/products?category=Electronics')
        data = response.get_json()
        assert all(p['category'] == 'Electronics' for p in data)

    def test_get_single_product(self, client):
        """GET /api/products/1 returns the correct product."""
        response = client.get('/api/products/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1

    def test_get_nonexistent_product_returns_404(self, client):
        """GET /api/products/9999 should return 404."""
        response = client.get('/api/products/9999')
        assert response.status_code == 404

    def test_search_products(self, client):
        """GET /api/products/search?q=headphones finds results."""
        response = client.get('/api/products/search?q=headphones')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0

    def test_search_empty_query(self, client):
        """Empty search returns empty list."""
        response = client.get('/api/products/search?q=')
        data = response.get_json()
        assert data == []

    def test_search_no_results(self, client):
        """Searching for gibberish returns empty list."""
        response = client.get('/api/products/search?q=xyznonexistent123')
        data = response.get_json()
        assert data == []


# ─── Category Tests ────────────────────────────────────────────────

class TestCategories:
    """What sections does the menu have?"""

    def test_list_categories(self, client):
        response = client.get('/api/categories')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert 'Electronics' in data


# ─── Cart Tests ────────────────────────────────────────────────────

class TestCart:
    """Can we order and manage items?"""

    def test_add_to_cart(self, client):
        """POST /api/cart adds an item."""
        response = client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 1,
            'quantity': 2
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True

    def test_view_cart(self, client):
        """After adding, we can see the item in the cart."""
        # Add an item first
        client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 1,
            'quantity': 2
        })
        # View the cart
        response = client.get('/api/cart/test-session')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['items']) == 1
        assert data['items'][0]['quantity'] == 2
        assert data['total'] > 0

    def test_add_same_item_increases_quantity(self, client):
        """Adding the same item twice should increase quantity."""
        client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 1,
            'quantity': 1
        })
        client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 1,
            'quantity': 3
        })
        response = client.get('/api/cart/test-session')
        data = response.get_json()
        assert data['items'][0]['quantity'] == 4

    def test_remove_from_cart(self, client):
        """DELETE /api/cart/:id removes the item."""
        client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 1,
            'quantity': 1
        })
        # Get cart to find item ID
        cart = client.get('/api/cart/test-session').get_json()
        item_id = cart['items'][0]['id']

        response = client.delete(f'/api/cart/{item_id}')
        assert response.status_code == 200

        # Verify empty
        cart = client.get('/api/cart/test-session').get_json()
        assert len(cart['items']) == 0

    def test_add_to_cart_missing_fields(self, client):
        """Missing required fields should return 400."""
        response = client.post('/api/cart', json={
            'session_id': 'test-session'
            # missing product_id
        })
        assert response.status_code == 400

    def test_add_nonexistent_product_to_cart(self, client):
        """Adding a product that doesn't exist should return 404."""
        response = client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 99999,
            'quantity': 1
        })
        assert response.status_code == 404

    def test_update_cart_quantity(self, client):
        """PUT /api/cart/:id updates the quantity."""
        client.post('/api/cart', json={
            'session_id': 'test-session',
            'product_id': 1,
            'quantity': 1
        })
        cart = client.get('/api/cart/test-session').get_json()
        item_id = cart['items'][0]['id']

        response = client.put(f'/api/cart/{item_id}', json={'quantity': 5})
        assert response.status_code == 200

        cart = client.get('/api/cart/test-session').get_json()
        assert cart['items'][0]['quantity'] == 5


# ─── Order Tests ───────────────────────────────────────────────────

class TestOrders:
    """Can we finalize a purchase?"""

    def test_place_order(self, client):
        """POST /api/orders creates an order from the cart."""
        # Add items to cart first
        client.post('/api/cart', json={
            'session_id': 'order-test',
            'product_id': 1,
            'quantity': 1
        })
        client.post('/api/cart', json={
            'session_id': 'order-test',
            'product_id': 2,
            'quantity': 2
        })

        # Place the order
        response = client.post('/api/orders', json={
            'session_id': 'order-test',
            'customer_name': 'Jane Doe',
            'customer_email': 'jane@example.com',
            'address': '123 Main Street',
            'city': 'Portland',
            'zip_code': '97201'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['customer_name'] == 'Jane Doe'
        assert data['total'] > 0
        assert len(data['items']) == 2

    def test_place_order_clears_cart(self, client):
        """After ordering, the cart should be empty."""
        client.post('/api/cart', json={
            'session_id': 'clear-test',
            'product_id': 1,
            'quantity': 1
        })
        client.post('/api/orders', json={
            'session_id': 'clear-test',
            'customer_name': 'John',
            'customer_email': 'john@example.com',
            'address': '456 Oak Ave',
            'city': 'Seattle',
            'zip_code': '98101'
        })
        cart = client.get('/api/cart/clear-test').get_json()
        assert len(cart['items']) == 0

    def test_order_empty_cart_fails(self, client):
        """Ordering with an empty cart should fail."""
        response = client.post('/api/orders', json={
            'session_id': 'empty-cart',
            'customer_name': 'Nobody',
            'customer_email': 'no@example.com',
            'address': 'Nowhere',
            'city': 'Void',
            'zip_code': '00000'
        })
        assert response.status_code == 400

    def test_get_order_details(self, client):
        """GET /api/orders/:id returns the full order."""
        # Place an order first
        client.post('/api/cart', json={
            'session_id': 'detail-test',
            'product_id': 1,
            'quantity': 1
        })
        order_response = client.post('/api/orders', json={
            'session_id': 'detail-test',
            'customer_name': 'Alice',
            'customer_email': 'alice@example.com',
            'address': '789 Pine St',
            'city': 'Denver',
            'zip_code': '80201'
        })
        order_id = order_response.get_json()['id']

        response = client.get(f'/api/orders/{order_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['customer_name'] == 'Alice'
        assert len(data['items']) > 0

    def test_order_missing_fields(self, client):
        """Missing required fields should return 400."""
        response = client.post('/api/orders', json={
            'session_id': 'test',
            'customer_name': 'Test'
            # Missing email, address, etc.
        })
        assert response.status_code == 400
