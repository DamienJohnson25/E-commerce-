import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from frontend

stripe.api_key = ""

@app.post("/create-checkout-session")
def create_checkout_session():
    data = request.json
    line_items = []

    # Build line items from cart
    for item in data.get("cart", []):
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": item["name"],
                    "images": [item.get("image_url", "")],
                },
                "unit_amount": int(item["price"] * 100),
            },
            "quantity": item["quantity"],
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:5173/checkout-success",
            cancel_url="http://localhost:5173/cart"
        )
        return jsonify({"url": session.url})

    except Exception as e:
        # 🔥 THIS IS THE IMPORTANT PART YOU ASKED FOR
        print("STRIPE ERROR:", e)
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    app.run(port=5000)
    