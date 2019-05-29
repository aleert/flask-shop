import factory.fuzzy

from models import Product
import fixtures
from app import app


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    title = factory.Faker('text', max_nb_chars=50)
    description = factory.Faker('text', max_nb_chars=250)
    price = factory.Faker('random_int', min=1)
    availability = factory.Faker('random_int', max=15)
    img_url = factory.fuzzy.FuzzyChoice(fixtures.product_images)


def populate_db(db, n_products: int=15) -> None:
    with app.app_context():
        products = [ProductFactory() for _ in range(n_products)]
        db.create_all()
        db.session.add_all(products)
        db.session.commit()
