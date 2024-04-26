from flask import Flask, render_template, request, redirect, url_for, send_file, make_response, session
from products import PRODUCTS

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    if 'cart' not in session:
        session['cart'] = []
        session.modified = True
    return render_template('index.html', products=PRODUCTS)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    
    total_price = sum(float(item['product']['price'].replace('$', '')) * item['quantity'] for item in cart)
    
    for i in cart:
        i['product']['price_count'] = float(i['product']['price'].replace('$', '')) * i['quantity']

    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    
    selected_product = next((product for product in PRODUCTS if product['id'] == product_id), None)

    if selected_product:

        for item in session['cart']:
            if item['product']['id'] == product_id:
                item['quantity'] += quantity
                break
        else:
            session['cart'].append({'product': selected_product, 'quantity': quantity})
        
        print(session['cart'])
        
        session.modified = True

    return redirect('/')

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    
    if cart:
        print("cart is not ")
        for i in cart:
            if i['product']['id'] == product_id:
                cart.remove(i)
                break

    session.modified = True
    
    return redirect('/cart')


if __name__ == '__main__':
    app.run(debug=True)
