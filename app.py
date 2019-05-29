from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


csrf = CSRFProtect()


def create_app(database):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bgnti84;jv_d-0ngr8gvhk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf.init_app(app)
    with app.app_context():
        database.init_app(app)
    CORS(app)

    return app


db = SQLAlchemy()
app = create_app(db)


import routes
import models

from populate_db import populate_db
populate_db(db, n_products=25)


if __name__ == '__main__':

    app.run(debug=True)
