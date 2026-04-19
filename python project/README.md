# 🛍️ ShopWave — E-Commerce Platform
### Python Flask · College Project

A clean, minimalist e-commerce web app built with Python (Flask).

---

## ✨ Features

| Feature | Details |
|---|---|
| 🏠 Homepage | Hero section, featured products, category grid |
| 🛒 Shop | Filter by category, search, sort by price / rating |
| 📄 Product Detail | Description, quantity picker, related products |
| 🛍️ Cart | Add / remove / update quantities |
| 💳 Checkout | Delivery form + demo payment flow |
| 📦 Orders | View your order history |
| ♡ Wishlist | Save products for later |
| 🔐 Auth | Login & Register with session management |
| 🔍 Live Search | Instant results in the nav bar |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8 or newer
- pip (comes with Python)

---

### Step 1 — Clone / Download the project

If you downloaded a ZIP, extract it. Then open a terminal and navigate into the folder:

```bash
cd ecommerce
```

---

### Step 2 — Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal prompt.

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask (the only dependency).

---

### Step 4 — Run the app

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Step 5 — Open in browser

Go to: **http://127.0.0.1:5000**

---

## 🔑 Demo Accounts

| Username | Password |
|---|---|
| `demo` | `demo123` |
| `admin` | `admin123` |

You can also register a new account from the Register page.

---

## 📁 Project Structure

```
ecommerce/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   ├── base.html           # Shared layout (nav, footer, flash)
│   ├── index.html          # Homepage
│   ├── products.html       # Product listing with filters
│   ├── product_detail.html # Single product page
│   ├── cart.html           # Shopping cart
│   ├── checkout.html       # Checkout form
│   ├── order_success.html  # Order confirmation
│   ├── orders.html         # Order history
│   ├── wishlist.html       # Saved items
│   ├── login.html          # Login page
│   └── register.html       # Register page
└── static/
    ├── css/
    │   └── style.css       # All styles
    └── js/
        └── main.js         # Live search, animations
```

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Fonts:** Cormorant Garamond + DM Sans (Google Fonts)
- **Data:** In-memory (no database needed)

---

## 📝 Notes for Submission

- All data (products, users, orders) is stored in-memory. It resets when you restart the server — this is intentional for a college project demo.
- No external database is required.
- The payment form is a UI demo only — no real transactions are processed.

---

*Built with ♥ using Python & Flask*
