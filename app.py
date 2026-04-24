from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
import logging

app = Flask(__name__)
app.secret_key = "nexus_tech_super_secret"

# Configure professional logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NexusTech")

# Enhanced Sample products with realistic descriptions, images, ratings, and premium badges
products = [
    {"id": 1, "name": "Quantum Laptop Pro", "price": 120000, "category": "Laptops", "image": "/static/products/1.png", "desc": "16-core CPU, 32GB RAM, 1TB NVMe SSD", "rating": 4.8, "reviews": 124, "badge": "Bestseller"},
    {"id": 2, "name": "NexusPhone X", "price": 85000, "category": "Phones", "image": "/static/products/2.png", "desc": "6.7' OLED, 108MP Camera, All-day Battery", "rating": 4.9, "reviews": 342, "badge": "New Release"},
    {"id": 3, "name": "AeroNoise Headphones", "price": 25000, "category": "Accessories", "image": "/static/products/3.png", "desc": "Active Noise Cancellation, Hi-Res Audio", "rating": 4.7, "reviews": 89},
    {"id": 4, "name": "Titanium Smart Watch", "price": 15000, "category": "Accessories", "image": "/static/products/4.png", "desc": "Advanced Health tracking, 7-day battery", "rating": 4.6, "reviews": 210, "badge": "Save 15%"},
    {"id": 5, "name": "Creator Studio Monitor", "price": 45000, "category": "Accessories", "image": "/static/products/5.png", "desc": "27-inch 4K UHD, Color Accurate display", "rating": 4.9, "reviews": 56},
    {"id": 6, "name": "LiteBook Air", "price": 75000, "category": "Laptops", "image": "/static/products/6.png", "desc": "Ultra-lightweight, 18-hour battery life", "rating": 4.5, "reviews": 178},
    {"id": 7, "name": "NexusPad Tablet", "price": 55000, "category": "Phones", "image": "/static/products/7.png", "desc": "11-inch screen, perfect for productivity", "rating": 4.7, "reviews": 112},
    {"id": 8, "name": "MechKey Pro Keyboard", "price": 12000, "category": "Accessories", "image": "/static/products/8.png", "desc": "Tactile mechanical switches, RGB backlit", "rating": 4.8, "reviews": 431},
    {"id": 9, "name": "Omni Console X", "price": 49999, "category": "Gaming", "image": "/static/products/9.png", "desc": "Next-gen gaming with 4K 120fps support", "rating": 4.9, "reviews": 890, "badge": "Hot Item"},
    {"id": 10, "name": "Aura Smart Speaker", "price": 8999, "category": "Smart Home", "image": "/static/products/10.png", "desc": "Voice controlled assistant with room-filling sound", "rating": 4.4, "reviews": 320},
    {"id": 11, "name": "Pro Gaming Mouse", "price": 6500, "category": "Gaming", "image": "/static/products/11.png", "desc": "25K DPI sensor, ultra-lightweight design", "rating": 4.8, "reviews": 512},
    {"id": 12, "name": "Security Cam 360", "price": 4500, "category": "Smart Home", "image": "/static/products/12.png", "desc": "1080p HD, night vision, motion tracking", "rating": 4.5, "reviews": 245}
]

# Mock Databases for complete e-commerce features
users_db = {} # username: {"password": "pwd", "email": "email", "name": "name"}
orders_db = [] # List of order dicts
promo_codes = {"NEXUS20": 0.20, "WELCOME10": 0.10, "DEV50": 0.50}

import random

def get_product(product_id):
    return next((p for p in products if p["id"] == product_id), None)

def get_related_products(category, exclude_id, count=3):
    related = [p for p in products if p['category'] == category and p['id'] != exclude_id]
    if len(related) < count:
        related += [p for p in products if p['id'] != exclude_id and p not in related]
    random.shuffle(related)
    return related[:count]

@app.before_request
def ensure_session():
    """Ensure every user gets their own session state."""
    session.permanent = True
    if 'cart' not in session: session['cart'] = []
    if 'wishlist' not in session: session['wishlist'] = []
    if 'discount' not in session: session['discount'] = 0
    if 'promo_code' not in session: session['promo_code'] = None
    
    # Auto-sync cart items with latest catalog images to prevent stale cache
    if 'cart' in session:
        cart_updated = False
        for item in session['cart']:
            current_product = get_product(item['id'])
            if current_product and item.get('image') != current_product['image']:
                item['image'] = current_product['image']
                cart_updated = True
        if cart_updated:
            session.modified = True

@app.route('/')
def home():
    logger.info(f"Home page accessed by IP: {request.remote_addr}")
    
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', 'All')
    sort_by = request.args.get('sort', 'default')
    
    filtered_products = products.copy()
    
    if category_filter != 'All':
        filtered_products = [p for p in filtered_products if p['category'] == category_filter]
        
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower() or search_query in p['desc'].lower()]
        
    if sort_by == 'price_asc':
        filtered_products.sort(key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'top_rated':
        filtered_products.sort(key=lambda x: x['rating'], reverse=True)
        
    return render_template('index.html', 
                           products=filtered_products, 
                           cart=session.get('cart', []),
                           current_category=category_filter,
                           search_query=request.args.get('search', ''),
                           current_sort=sort_by,
                           wishlist=session.get('wishlist', []),
                           user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db and users_db[username]['password'] == password:
            session['user'] = users_db[username]
            flash(f"Welcome back, {users_db[username]['name']}!", "success")
            return redirect(url_for('home'))
        flash("Invalid username or password.", "danger")
    return render_template('auth.html', mode='login', cart=session.get('cart', []))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in users_db:
            flash("Username already exists.", "danger")
        else:
            users_db[username] = {
                "username": username,
                "password": request.form.get('password'),
                "email": request.form.get('email'),
                "name": request.form.get('name')
            }
            session['user'] = users_db[username]
            flash("Account successfully created!", "success")
            return redirect(url_for('home'))
    return render_template('auth.html', mode='register', cart=session.get('cart', []))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))
    user_orders = [o for o in orders_db if o['username'] == session['user']['username']]
    return render_template('profile.html', user=session['user'], orders=user_orders, cart=session.get('cart', []))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        return render_template('404.html'), 404
    related = get_related_products(product['category'], product_id)
    return render_template('product.html', product=product, related=related, cart=session.get('cart', []), wishlist=session.get('wishlist', []), user=session.get('user'))

@app.route('/wishlist/toggle/<int:product_id>')
def toggle_wishlist(product_id):
    wishlist = session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        flash("Removed from wishlist.", "success")
    else:
        wishlist.append(product_id)
        flash("Added to wishlist ❤️", "success")
    session['wishlist'] = wishlist
    session.modified = True
    return redirect(request.referrer or url_for('home'))

@app.route('/wishlist')
def view_wishlist():
    wishlist_ids = session.get('wishlist', [])
    wishlist_products = [get_product(pid) for pid in wishlist_ids if get_product(pid)]
    return render_template('wishlist.html', products=wishlist_products, cart=session.get('cart', []), user=session.get('user'))

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    product = get_product(product_id)
    if product:
        cart = session.get('cart', [])
        
        # Check if item is already in cart, if so, increase quantity
        found = False
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] = item.get('quantity', 1) + 1
                found = True
                break
                
        if not found:
            product_copy = product.copy()
            product_copy['quantity'] = 1
            cart.append(product_copy)
            
        session['cart'] = cart
        session.modified = True
        logger.info(f"Added to cart: {product['name']}")
        flash(f"✅ {product['name']} was successfully added to your cart!", "success")
    else:
        logger.warning(f"Failed to add product: ID {product_id} not found.")
        flash("❌ Product not found.", "danger")
        
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    subtotal = sum(item["price"] * item.get("quantity", 1) for item in cart)
    discount_amount = subtotal * session.get('discount', 0)
    total = subtotal - discount_amount
    return render_template('cart.html', cart=cart, subtotal=subtotal, discount=discount_amount, total=total, promo_code=session.get('promo_code'), user=session.get('user'))

@app.route('/apply_promo', methods=['POST'])
def apply_promo():
    code = request.form.get('promo_code', '').upper()
    if code in promo_codes:
        session['promo_code'] = code
        session['discount'] = promo_codes[code]
        flash(f"Promo code {code} applied successfully! You saved {int(promo_codes[code]*100)}%.", "success")
    else:
        flash("Invalid promo code.", "danger")
    return redirect(request.referrer or url_for('view_cart'))

@app.route('/remove_promo')
def remove_promo():
    session.pop('promo_code', None)
    session['discount'] = 0
    flash("Promo code removed.", "success")
    return redirect(request.referrer or url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('home'))
        
    subtotal = sum(item["price"] * item.get("quantity", 1) for item in cart)
    discount_amount = subtotal * session.get('discount', 0)
    total = subtotal - discount_amount
    
    if request.method == 'POST':
        # Process Order
        order_id = f"ORD-{random.randint(10000, 99999)}"
        new_order = {
            "order_id": order_id,
            "username": session['user']['username'] if 'user' in session else "Guest",
            "items": cart.copy(),
            "total": total,
            "status": "Processing",
            "shipping_address": request.form.get('address', 'Unknown')
        }
        orders_db.append(new_order)
        
        # Clear Cart
        session['cart'] = []
        session['discount'] = 0
        session.pop('promo_code', None)
        session.modified = True
        logger.info(f"Order {order_id} placed successfully. Total: ₹{total}")
        flash(f"🎉 Order {order_id} successfully placed! Thank you.", "success")
        return redirect(url_for('home'))
        
    return render_template('checkout.html', cart=cart, subtotal=subtotal, discount=discount_amount, total=total, user=session.get('user'))

@app.route('/api/health')
def health_check():
    """Endpoint for DevOps CI/CD pipeline to verify application is running."""
    return jsonify({"status": "healthy", "version": "2.0.0", "service": "NexusTech Web"}), 200

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler."""
    logger.warning(f"404 Error - Page not found: {request.url}")
    return render_template('404.html'), 404

if __name__ == "__main__":
    logger.info("Starting NexusTech E-Commerce Server...")
    # debug=True allows hot-reloading locally, should be disabled in production
    app.run(host="0.0.0.0", port=5000, debug=True)