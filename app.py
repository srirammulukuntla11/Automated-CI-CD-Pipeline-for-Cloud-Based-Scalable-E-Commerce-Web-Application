from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "nexus_tech_super_secret"

# Sample products
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 2000},
    {"id": 4, "name": "Smart Watch", "price": 5000}
]

cart = []

@app.route('/')
def home():
    return render_template('index.html', products=products, cart=cart)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    for product in products:
        if product["id"] == product_id:
            cart.append(product)
            flash(f"✅ {product['name']} was successfully added to your cart!", "success")
            break
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    total = sum(item["price"] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove/<int:index>')
def remove_item(index):
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        flash(f"🗑️ {removed_item['name']} has been removed from your cart.", "success")
    return redirect(url_for('view_cart'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)