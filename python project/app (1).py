from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'shopwave_secret_key_2024'

# ── In-memory "database" ──────────────────────────────────────────────────────

PRODUCTS = [
    # ── Tech ──────────────────────────────────────────────────────────────────
    {"id": 1,  "name": "Wireless Earbuds Pro",       "price": 12499,  "category": "Tech",        "photo": "https://images.unsplash.com/photo-1590658268268-d6fc7aa8d821?auto=format&fit=crop&w=600&q=80", "description": "40-hour battery, adaptive noise cancellation, and premium sound in a pebble-sized case.", "stock": 30, "rating": 4.8, "reviews": 543},
    {"id": 2,  "name": "Smart Watch Series 8",       "price": 24999,  "category": "Tech",        "photo": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80", "description": "Always-on AMOLED display, SpO2 sensor, 14-day battery life and 5ATM water resistance.", "stock": 18, "rating": 4.7, "reviews": 311},
    {"id": 3,  "name": "Mechanical Keyboard",        "price": 8999,   "category": "Tech",        "photo": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80", "description": "TKL layout, Cherry MX switches, per-key RGB and aircraft-grade aluminium top plate.", "stock": 22, "rating": 4.9, "reviews": 189},
    {"id": 4,  "name": "Bluetooth Speaker",          "price": 5499,   "category": "Tech",        "photo": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=600&q=80", "description": "360° surround sound, IPX7 waterproof, 24-hour playtime. Perfect for outdoor use.", "stock": 40, "rating": 4.6, "reviews": 274},
    {"id": 5,  "name": "Bamboo Wireless Charger",    "price": 2199,   "category": "Tech",        "photo": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=600&q=80", "description": "15W Qi2 fast-charging pad in natural bamboo. Compatible with all Qi devices.", "stock": 35, "rating": 4.5, "reviews": 192},
    {"id": 6,  "name": "Gaming Mouse",               "price": 3799,   "category": "Tech",        "photo": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80", "description": "25,600 DPI optical sensor, 11 programmable buttons, ultra-lightweight 59g shell.", "stock": 28, "rating": 4.7, "reviews": 428},
    # ── Home ──────────────────────────────────────────────────────────────────
    {"id": 7,  "name": "Minimal Desk Lamp",          "price": 3299,   "category": "Home",        "photo": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80", "description": "Sleek aluminium arm lamp with warm LED and stepless dimmer. Perfect for late-night work.", "stock": 15, "rating": 4.8, "reviews": 124},
    {"id": 8,  "name": "Indoor Monstera Plant",      "price": 1199,   "category": "Home",        "photo": "https://images.unsplash.com/photo-1463936575829-25148e1db1b8?auto=format&fit=crop&w=600&q=80", "description": "Live Swiss Cheese plant in a 14cm nursery pot. Thrives in indirect light, low maintenance.", "stock": 20, "rating": 4.9, "reviews": 87},
    {"id": 9,  "name": "Linen Throw Cushion",        "price": 1599,   "category": "Home",        "photo": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80", "description": "45×45cm stonewashed linen cover with feather-down insert. Available in 6 natural tones.", "stock": 50, "rating": 4.7, "reviews": 211},
    {"id": 10, "name": "Scented Soy Candle Set",     "price": 899,    "category": "Home",        "photo": "https://images.unsplash.com/photo-1603905751371-4bb14974b859?auto=format&fit=crop&w=600&q=80", "description": "Set of 3 hand-poured soy candles — Sandalwood, Jasmine & Sea Salt. 40-hour burn each.", "stock": 60, "rating": 4.8, "reviews": 305},
    {"id": 11, "name": "Rattan Wall Mirror",         "price": 4499,   "category": "Home",        "photo": "https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=600&q=80", "description": "60cm round mirror with handwoven natural rattan frame. Adds warmth to any room.", "stock": 12, "rating": 4.6, "reviews": 68},
    # ── Kitchen ───────────────────────────────────────────────────────────────
    {"id": 12, "name": "Ceramic Pour-Over Set",      "price": 2799,   "category": "Kitchen",     "photo": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80", "description": "Hand-thrown ceramic dripper with matching carafe and filters. For the ritual coffee drinker.", "stock": 8,  "rating": 4.9, "reviews": 89},
    {"id": 13, "name": "Cast Iron Skillet 26cm",     "price": 3999,   "category": "Kitchen",     "photo": "https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&w=600&q=80", "description": "Pre-seasoned cast iron with helper handle. Works on all hobs including induction.", "stock": 14, "rating": 4.8, "reviews": 163},
    {"id": 14, "name": "Handmade Ceramic Mug",       "price": 699,    "category": "Kitchen",     "photo": "https://images.unsplash.com/photo-1514866726338-ead4db3aef2b?auto=format&fit=crop&w=600&q=80", "description": "350ml stoneware mug, wheel-thrown with speckled glaze finish. Microwave & dishwasher safe.", "stock": 75, "rating": 4.7, "reviews": 412},
    {"id": 15, "name": "Glass Water Bottle 700ml",   "price": 1299,   "category": "Kitchen",     "photo": "https://images.unsplash.com/photo-1602143407259-b8c5e9e5d928?auto=format&fit=crop&w=600&q=80", "description": "Borosilicate glass with silicone sleeve, bamboo lid. Dishwasher safe, leak-proof.", "stock": 60, "rating": 4.8, "reviews": 267},
    {"id": 16, "name": "Acacia Wood Cutting Board",  "price": 2199,   "category": "Kitchen",     "photo": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80", "description": "Extra-large 45×30cm acacia board with juice groove and integrated handle.", "stock": 22, "rating": 4.7, "reviews": 97},
    # ── Accessories ───────────────────────────────────────────────────────────
    {"id": 17, "name": "Leather Bifold Wallet",      "price": 1899,   "category": "Accessories", "photo": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=600&q=80", "description": "Full-grain vegetable-tanned leather. Ages beautifully. 8 card slots + 2 cash pockets.", "stock": 40, "rating": 4.8, "reviews": 308},
    {"id": 18, "name": "Canvas Tote Bag",            "price": 899,    "category": "Accessories", "photo": "https://images.unsplash.com/photo-1591085686350-798c0f9fad46?auto=format&fit=crop&w=600&q=80", "description": "Heavy-duty 12oz canvas with leather handles and internal zip pocket. Fits A4 and laptop.", "stock": 80, "rating": 4.6, "reviews": 145},
    {"id": 19, "name": "Modular Travel Backpack",    "price": 7999,   "category": "Accessories", "photo": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80", "description": "30L capacity with magnetic modular pockets. Recycled ripstop nylon, 15\" laptop sleeve.", "stock": 9,  "rating": 4.9, "reviews": 421},
    {"id": 20, "name": "Polarised Sunglasses",       "price": 2499,   "category": "Accessories", "photo": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=600&q=80", "description": "UV400 polarised lenses in acetate frames. Includes hardcase and cleaning cloth.", "stock": 35, "rating": 4.5, "reviews": 193},
    # ── Sports & Fitness ──────────────────────────────────────────────────────
    {"id": 21, "name": "Running Shoes — Air Max",    "price": 6999,   "category": "Sports",      "photo": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80", "description": "Responsive foam midsole, breathable mesh upper. Neutral support for daily training.", "stock": 24, "rating": 4.7, "reviews": 612},
    {"id": 22, "name": "Yoga Mat — 6mm",             "price": 1799,   "category": "Sports",      "photo": "https://images.unsplash.com/photo-1601925228843-02e77f5b89ed?auto=format&fit=crop&w=600&q=80", "description": "Eco-friendly TPE mat with alignment lines, non-slip surface and carry strap.", "stock": 45, "rating": 4.8, "reviews": 389},
    {"id": 23, "name": "Adjustable Dumbbell 10kg",   "price": 3499,   "category": "Sports",      "photo": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "description": "Quick-select dial adjusts from 2–10kg in 2kg steps. Replaces 5 pairs of dumbbells.", "stock": 16, "rating": 4.6, "reviews": 174},
    {"id": 24, "name": "Insulated Sports Bottle",    "price": 1499,   "category": "Sports",      "photo": "https://images.unsplash.com/photo-1588776814546-ec7e074fa3e7?auto=format&fit=crop&w=600&q=80", "description": "750ml double-wall vacuum insulated. Keeps cold 24h, hot 12h. BPA-free stainless.", "stock": 55, "rating": 4.9, "reviews": 501},
]

USERS = {
    "admin": {"password": "admin123", "name": "Admin User", "email": "admin@shopwave.com"},
    "demo":  {"password": "demo123",  "name": "Demo User",  "email": "demo@shopwave.com"},
}

ORDERS = []  # { id, user, items, total, status, date }

# ── Helpers ───────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to continue.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_cart():
    return session.get('cart', {})

def cart_count():
    return sum(get_cart().values())

def cart_total():
    cart = get_cart()
    total = 0
    for pid, qty in cart.items():
        p = next((x for x in PRODUCTS if x['id'] == int(pid)), None)
        if p:
            total += p['price'] * qty
    return round(total, 2)

@app.context_processor
def inject_globals():
    return dict(cart_count=cart_count(), logged_in='user' in session,
                username=session.get('user', ''))

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    featured = PRODUCTS[:6]
    categories = list({p['category'] for p in PRODUCTS})
    return render_template('index.html', featured=featured, categories=categories,
                           total_products=len(PRODUCTS))

@app.route('/products')
def products():
    category = request.args.get('category', '')
    search   = request.args.get('q', '').lower()
    sort     = request.args.get('sort', 'default')
    filtered = PRODUCTS[:]
    if category:
        filtered = [p for p in filtered if p['category'] == category]
    if search:
        filtered = [p for p in filtered if search in p['name'].lower() or search in p['description'].lower()]
    if sort == 'price_asc':
        filtered.sort(key=lambda x: x['price'])
    elif sort == 'price_desc':
        filtered.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'rating':
        filtered.sort(key=lambda x: x['rating'], reverse=True)
    categories = list({p['category'] for p in PRODUCTS})
    return render_template('products.html', products=filtered, categories=categories,
                           active_category=category, search=search, sort=sort)

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != pid][:3]
    return render_template('product_detail.html', product=product, related=related)

@app.route('/cart')
def cart():
    cart_data = get_cart()
    items = []
    for pid, qty in cart_data.items():
        p = next((x for x in PRODUCTS if x['id'] == int(pid)), None)
        if p:
            items.append({**p, 'qty': qty, 'subtotal': round(p['price'] * qty, 2)})
    return render_template('cart.html', items=items, total=cart_total())

@app.route('/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    qty = int(request.form.get('qty', 1))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))

@app.route('/cart/update', methods=['POST'])
def update_cart():
    pid = request.form.get('pid')
    qty = int(request.form.get('qty', 1))
    cart = get_cart()
    if qty <= 0:
        cart.pop(str(pid), None)
    else:
        cart[str(pid)] = qty
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/remove/<pid>')
def remove_from_cart(pid):
    cart = get_cart()
    cart.pop(str(pid), None)
    session['cart'] = cart
    flash('Item removed.', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_data = get_cart()
    if not cart_data:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('products'))
    items = []
    for pid, qty in cart_data.items():
        p = next((x for x in PRODUCTS if x['id'] == int(pid)), None)
        if p:
            items.append({**p, 'qty': qty, 'subtotal': round(p['price'] * qty, 2)})
    if request.method == 'POST':
        order = {
            'id': len(ORDERS) + 1001,
            'user': session['user'],
            'items': items,
            'total': cart_total(),
            'status': 'Confirmed',
            'date': '2024-12-15',
            'address': request.form.get('address', ''),
            'name': request.form.get('name', ''),
        }
        ORDERS.append(order)
        session['cart'] = {}
        flash(f'Order #{order["id"]} placed successfully! 🎉', 'success')
        return redirect(url_for('order_success', oid=order['id']))
    return render_template('checkout.html', items=items, total=cart_total())

@app.route('/order/success/<int:oid>')
@login_required
def order_success(oid):
    order = next((o for o in ORDERS if o['id'] == oid), None)
    return render_template('order_success.html', order=order)

@app.route('/orders')
@login_required
def orders():
    user_orders = [o for o in ORDERS if o['user'] == session['user']]
    return render_template('orders.html', orders=user_orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = username
            session['user_name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        if username in USERS:
            flash('Username already taken.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        else:
            USERS[username] = {'password': password, 'name': name, 'email': email}
            session['user'] = username
            session['user_name'] = name
            flash(f'Account created! Welcome, {name}!', 'success')
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/wishlist')
@login_required
def wishlist():
    wish = session.get('wishlist', [])
    items = [p for p in PRODUCTS if p['id'] in wish]
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/toggle/<int:pid>')
@login_required
def toggle_wishlist(pid):
    wish = session.get('wishlist', [])
    if pid in wish:
        wish.remove(pid)
        flash('Removed from wishlist.', 'info')
    else:
        wish.append(pid)
        flash('Added to wishlist! ♡', 'success')
    session['wishlist'] = wish
    return redirect(request.referrer or url_for('products'))

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').lower()
    results = [p for p in PRODUCTS if q in p['name'].lower()][:5]
    return jsonify([{'id': p['id'], 'name': p['name'], 'price': p['price']} for p in results])

if __name__ == '__main__':
    app.run(debug=True)
