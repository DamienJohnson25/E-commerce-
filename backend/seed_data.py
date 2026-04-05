"""
seed_data.py — Populate the Database with Sample Products
==========================================================
Think of this as "stocking the shelves" before the store opens.
Run this once: python seed_data.py
"""

from models import init_db, get_db

PRODUCTS = [
    # ── Electronics ──
    {
        "name": "Wireless Noise-Cancelling Headphones",
        "description": "Premium over-ear headphones with active noise cancellation, 30-hour battery life, and ultra-soft memory foam cushions. Perfect for commuting, travel, or deep focus work sessions.",
        "price": 79.99,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
        "category": "Electronics",
        "stock": 45,
        "featured": 1,
        "rating": 4.7
    },
    {
        "name": "Portable Bluetooth Speaker",
        "description": "Waterproof portable speaker with 360-degree sound, 12-hour battery, and built-in microphone. Take your music anywhere — beach, camping, or backyard barbecues.",
        "price": 49.99,
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600",
        "category": "Electronics",
        "stock": 60,
        "featured": 0,
        "rating": 4.4
    },
    {
        "name": "Mechanical Keyboard",
        "description": "RGB backlit mechanical keyboard with tactile switches, programmable macros, and aircraft-grade aluminum frame. Your fingers will thank you.",
        "price": 129.99,
        "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=600",
        "category": "Electronics",
        "stock": 30,
        "featured": 1,
        "rating": 4.8
    },
    {
        "name": "USB-C Fast Charger",
        "description": "65W GaN charger with dual USB-C ports and one USB-A port. Charge your laptop and phone simultaneously. Compact enough to fit in your pocket.",
        "price": 34.99,
        "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600",
        "category": "Electronics",
        "stock": 100,
        "featured": 0,
        "rating": 4.5
    },
    # ── Clothing ──
    {
        "name": "Classic Denim Jacket",
        "description": "Timeless medium-wash denim jacket with brass button closures and adjustable waist tabs. Layered or solo, this piece works year-round.",
        "price": 89.99,
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600",
        "category": "Clothing",
        "stock": 25,
        "featured": 1,
        "rating": 4.6
    },
    {
        "name": "Cotton Crew T-Shirt — 3 Pack",
        "description": "Ultra-soft 100% combed cotton tees in black, white, and heather grey. Pre-shrunk, tagless comfort that gets softer with every wash.",
        "price": 29.99,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600",
        "category": "Clothing",
        "stock": 80,
        "featured": 0,
        "rating": 4.3
    },
    {
        "name": "Running Shoes — Cloud Series",
        "description": "Lightweight mesh running shoes with responsive cushioning and breathable upper. Designed for everyday runners who want comfort without sacrificing speed.",
        "price": 119.99,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
        "category": "Clothing",
        "stock": 35,
        "featured": 1,
        "rating": 4.7
    },
    # ── Home & Kitchen ──
    {
        "name": "Pour-Over Coffee Maker Set",
        "description": "Hand-blown borosilicate glass carafe with stainless steel mesh filter. Brew café-quality pour-over coffee at home. Includes 40 paper filters.",
        "price": 42.99,
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600",
        "category": "Home & Kitchen",
        "stock": 50,
        "featured": 1,
        "rating": 4.6
    },
    {
        "name": "Cast Iron Skillet — 12 Inch",
        "description": "Pre-seasoned cast iron skillet that goes from stovetop to oven. Even heat distribution, naturally non-stick, and built to last generations.",
        "price": 39.99,
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600",
        "category": "Home & Kitchen",
        "stock": 40,
        "featured": 0,
        "rating": 4.8
    },
    {
        "name": "Bamboo Cutting Board Set",
        "description": "Set of 3 organic bamboo cutting boards in small, medium, and large sizes. Knife-friendly, antimicrobial, and sourced from sustainable bamboo forests.",
        "price": 27.99,
        "image_url": "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=600",
        "category": "Home & Kitchen",
        "stock": 55,
        "featured": 0,
        "rating": 4.4
    },
    # ── Books ──
    {
        "name": "The Pragmatic Programmer",
        "description": "20th Anniversary Edition. A classic guide for developers who want to write better code, think more clearly, and build a career that lasts.",
        "price": 39.99,
        "image_url": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=600",
        "category": "Books",
        "stock": 70,
        "featured": 1,
        "rating": 4.9
    },
    {
        "name": "Design Patterns: A Visual Guide",
        "description": "Beautifully illustrated guide to the 23 Gang-of-Four design patterns. Learn with diagrams, real-world examples, and code in Python and JavaScript.",
        "price": 34.99,
        "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600",
        "category": "Books",
        "stock": 45,
        "featured": 0,
        "rating": 4.5
    },
    # ── Accessories ──
    {
        "name": "Leather Laptop Sleeve — 14 inch",
        "description": "Full-grain vegetable-tanned leather sleeve with soft microfiber lining. Slim-fit design with magnetic closure. Ages beautifully over time.",
        "price": 59.99,
        "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600",
        "category": "Accessories",
        "stock": 30,
        "featured": 0,
        "rating": 4.6
    },
    {
        "name": "Minimalist Analog Watch",
        "description": "Japanese quartz movement, sapphire crystal glass, and Italian leather strap. 38mm case diameter. Water resistant to 50 meters.",
        "price": 149.99,
        "image_url": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600",
        "category": "Accessories",
        "stock": 20,
        "featured": 1,
        "rating": 4.7
    },
    {
        "name": "Canvas Backpack",
        "description": "Waxed canvas daypack with padded laptop compartment, water bottle pockets, and YKK zippers. Built for daily commutes and weekend adventures.",
        "price": 69.99,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
        "category": "Accessories",
        "stock": 40,
        "featured": 0,
        "rating": 4.5
    },
]


def seed():
    """Insert all sample products into the database."""
    init_db()
    conn = get_db()

    # Clear existing data and reset auto-increment
    conn.execute('DELETE FROM order_items')
    conn.execute('DELETE FROM orders')
    conn.execute('DELETE FROM cart_items')
    conn.execute('DELETE FROM products')
    conn.execute("DELETE FROM sqlite_sequence WHERE name='products'")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='cart_items'")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='order_items'")

    for product in PRODUCTS:
        conn.execute('''
            INSERT INTO products (name, description, price, image_url, category, stock, featured, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['name'], product['description'], product['price'],
            product['image_url'], product['category'], product['stock'],
            product['featured'], product['rating']
        ))

    conn.commit()
    conn.close()
    print(f"✅ Database seeded with {len(PRODUCTS)} products!")


if __name__ == '__main__':
    seed()
