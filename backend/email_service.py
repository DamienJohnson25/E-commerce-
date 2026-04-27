"""
email_service.py — Send Transactional Emails via Brevo SMTP
=============================================================
This module handles all email sending for ShopVue.
It uses Brevo's SMTP relay, which is just a regular SMTP server —
Python's built-in smtplib knows how to talk to it.

Analogy: If your Flask app is a restaurant, this module is the
postal service. After an order is placed, the restaurant writes
a receipt letter and hands it to the postal service (Brevo),
who delivers it to the customer's mailbox (inbox).

SMTP credentials come from environment variables — never hardcoded.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ─── Brevo SMTP Configuration ─────────────────────────────────────
# These come from your Brevo dashboard: Settings → SMTP & API
SMTP_HOST = 'smtp-relay.brevo.com'
SMTP_PORT = 587  # STARTTLS encryption
SMTP_USER = os.environ.get('BREVO_SMTP_USER', '')     # Your Brevo login email
SMTP_KEY = os.environ.get('BREVO_SMTP_KEY', '')        # Your Brevo SMTP key
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', '')
SENDER_NAME = os.environ.get('SENDER_NAME', '')


def send_email(to_email, to_name, subject, html_body):
    """
    Send a single email via Brevo SMTP.
    Returns True on success, False on failure.
    """
    if not SMTP_USER or not SMTP_KEY:
        print("[EMAIL] SMTP credentials not configured — skipping email send")
        return False

    # Build the email message
    msg = MIMEMultipart('alternative')
    msg['From'] = f'{SENDER_NAME} <{SENDER_EMAIL}>'
    msg['To'] = f'{to_name} <{to_email}>'
    msg['Subject'] = subject

    # Attach the HTML body
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Connect to Brevo's SMTP server
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()                          # Encrypt the connection
        server.login(SMTP_USER, SMTP_KEY)          # Authenticate
        server.send_message(msg)                   # Send!
        server.quit()                              # Close connection
        print(f"[EMAIL] Sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"[EMAIL] Failed to send to {to_email}: {e}")
        return False


# ─── Email Templates ──────────────────────────────────────────────

def send_order_confirmation(order):
    """Send an order confirmation email with item details."""
    items_html = ''
    for item in order.get('items', []):
        items_html += f"""
        <tr>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;">{item['name']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;">{item['quantity']}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right;">${item['price']:.2f}</td>
        </tr>
        """

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#333;">
        <div style="background:#C8553D;color:white;padding:24px;text-align:center;">
            <h1 style="margin:0;font-size:22px;">Order Confirmed!</h1>
        </div>

        <div style="padding:24px;">
            <p>Hi {order['customer_name']},</p>
            <p>Thank you for your order! Here's a summary:</p>

            <table style="width:100%;border-collapse:collapse;margin:16px 0;">
                <thead>
                    <tr style="background:#f8f8f8;">
                        <th style="padding:8px 12px;text-align:left;">Item</th>
                        <th style="padding:8px 12px;text-align:center;">Qty</th>
                        <th style="padding:8px 12px;text-align:right;">Price</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>

            <div style="text-align:right;font-size:18px;font-weight:bold;margin:16px 0;">
                Total: ${order['total']:.2f}
            </div>

            <div style="background:#f8f8f8;padding:16px;border-radius:8px;margin:16px 0;">
                <strong>Shipping to:</strong><br>
                {order['address']}<br>
                {order['city']}, {order['zip_code']}
            </div>

            <p style="color:#888;font-size:13px;margin-top:24px;">
                Order #{order['id']} &middot; Placed on {order.get('created_at', 'today')}
            </p>
        </div>

        <div style="background:#f8f8f8;padding:16px;text-align:center;font-size:12px;color:#999;">
            ShopVue &middot; Thank you for shopping with us
        </div>
    </div>
    """

    return send_email(
        to_email=order['customer_email'],
        to_name=order['customer_name'],
        subject=f"ShopVue — Order #{order['id']} Confirmed!",
        html_body=html
    )


def send_welcome_email(name, email):
    """Send a welcome email after registration."""
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#333;">
        <div style="background:#C8553D;color:white;padding:24px;text-align:center;">
            <h1 style="margin:0;font-size:22px;">Welcome to ShopVue!</h1>
        </div>

        <div style="padding:24px;">
            <p>Hi {name},</p>
            <p>Your account has been created. You're all set to start shopping!</p>
            <p>Here's what you can do:</p>
            <ul>
                <li>Browse our product catalog</li>
                <li>Add items to your cart</li>
                <li>Place orders with fast checkout</li>
            </ul>
            <p>Happy shopping!</p>
        </div>

        <div style="background:#f8f8f8;padding:16px;text-align:center;font-size:12px;color:#999;">
            ShopVue &middot; Thank you for joining us
        </div>
    </div>
    """

    return send_email(
        to_email=email,
        to_name=name,
        subject="Welcome to ShopVue!",
        html_body=html
    )
