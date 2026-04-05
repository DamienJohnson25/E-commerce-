# 🛒 ShopVue — E-Commerce Application

A full-stack e-commerce application built with **Vue.js** (frontend), **Python Flask** (backend), and **SQLite** (database). Designed as a learning project that walks beginners through the entire development lifecycle.

## Quick Start

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Seed the Database
```bash
cd backend
python seed_data.py
```

### 3. Start the Backend Server
```bash
cd backend
python app.py
# → Running at http://localhost:5000
```

### 4. Install Frontend Dependencies (new terminal)
```bash
cd frontend
npm install
```

### 5. Start the Frontend Dev Server
```bash
cd frontend
npm run dev
# → Running at http://localhost:5173
```

### 6. Open in Browser
Visit **http://localhost:5173** and start shopping!

## Running Tests
```bash
# From project root
python -m pytest tests/test_backend.py -v
```

## Project Structure
```
ecommerce-app/
├── backend/           ← Python Flask API server
│   ├── app.py         ← Main server with all endpoints
│   ├── models.py      ← Database operations
│   ├── seed_data.py   ← Sample product data
│   └── shop.db        ← SQLite database (auto-created)
├── frontend/          ← Vue.js single-page application
│   ├── src/
│   │   ├── components/  ← Reusable UI pieces (NavBar, ProductCard)
│   │   ├── views/       ← Full pages (Home, Products, Cart, Checkout)
│   │   ├── store/       ← State management (Pinia)
│   │   └── router/      ← Page navigation
│   └── package.json
├── tests/             ← Backend test suite (23 tests)
└── docs/              ← Full development lifecycle guide
```

## Tech Stack
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Vue.js 3 + Vite | User interface |
| State | Pinia | Cart & product state management |
| Routing | Vue Router | Page navigation |
| Backend | Python Flask | REST API server |
| Database | SQLite | Data storage |
| Testing | pytest | Backend test suite |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/products | List all products |
| GET | /api/products/:id | Product details |
| GET | /api/products/search?q= | Search products |
| GET | /api/categories | List categories |
| POST | /api/cart | Add to cart |
| GET | /api/cart/:session | View cart |
| PUT | /api/cart/:id | Update quantity |
| DELETE | /api/cart/:id | Remove from cart |
| POST | /api/orders | Place order |
| GET | /api/orders/:id | Order details |

## Learning Guide
See **docs/DEVELOPMENT_GUIDE.md** for a comprehensive walkthrough of every development phase — from requirements gathering to deployment — with analogies and explanations for beginners.
