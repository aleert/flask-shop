import uuid

from sqlalchemy.ext.associationproxy import association_proxy

from app import db


uuid_key = lambda: str(uuid.uuid4())


class Cart(db.Model):
    id = db.Column(db.Unicode(36), default=uuid_key, primary_key=True)
    cart_products = db.relationship('CartProduct', backref='cart')

    products = association_proxy('cart_products', 'product')

    def total_price(self):
        total_price = 0
        for item in self.cart_products:
            total_price += item.product.price * item.quantity
        return total_price

    def __repr__(self):
        return '{0} cart for {1}'.format(self.id, str(self.total_price()))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(100))
    description = db.Column(db.UnicodeText)
    price = db.Column(db.DECIMAL(precision=2), db.CheckConstraint('price>0'))
    availability = db.Column(
        'availability',
        db.Integer,
        db.CheckConstraint('availability>=0'),
        default=0,
    )
    img_file_path = db.Column(db.Unicode(128), nullable=True)
    img_url = db.Column(db.Unicode(200))

    def __repr__(self):
        return '{0} {1:.2f}$'.format(self.title, self.price)


class CartProduct(db.Model):

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('product.id'),
        primary_key=True,
    )
    cart_id = db.Column(
        db.Unicode(36),
        db.ForeignKey('cart.id'),
        primary_key=True,
    )
    quantity = db.Column('quantity', db.Integer(), nullable=False)

    def __init__(self, product=None, quantity=1):
        self.product = product
        self.quantity = quantity

    product = db.relationship(Product, lazy='joined')

    def __repr__(self):
        return '{0} of {1} in {2} cart'.format(self.product, self.quantity, self.cart)

