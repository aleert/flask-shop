import sys
from json import JSONDecodeError

from flask import render_template, redirect, url_for
from flask import request
from flask import json

from app import db

from app import app
from models import Product, Cart, CartProduct


@app.route('/')
def product_list():
    page = request.args.get('page', type=int)
    products = Product.query.paginate(page, 5, False)
    next_url = url_for('product_list', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('product_list', page=products.prev_num) \
        if products.has_prev else None
    return render_template(
        'index.html',
        products=products.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/cart', methods=['GET', 'POST'])
def cart_view():
    if request.method == 'POST':
        cart = Cart()

        # check for malformed post
        try:
            products_data = json.loads(request.data, parse_int=int)
        except JSONDecodeError:
            return redirect(url_for('product_list'))

        # so we wont create actual empty Cart in db for every cart/ request when cart is empty
        if products_data.get('id') == '' and not products_data['products']:
            return url_for('cart_view', cart_id='0')

        products = Product.query.filter(Product.id.in_([*products_data['products']])).all()
        prod_dict = {int(product.id): product for product in products}
        for product_id, quantity in products_data['products'].items():
            cart.cart_products.append(CartProduct(prod_dict[int(product_id)], quantity=quantity))
        db.session.add(cart)
        db.session.commit()
        return url_for('cart_view', cart_id=cart.id)

    elif request.method == 'GET':
        if not request.args.get('cart_id'):
            return redirect(url_for('product_list'))

        cart = Cart()
        cart_id = request.args.get('cart_id')
        if cart_id != '0':
            cart = Cart.query.get_or_404(cart_id)
        return render_template('cart.html', cart=cart)

