import os
from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def initialize_models():
    from Server.Models.Customers import Customers
    from Server.Models.Transactions import Transactions
    from Server.Models.LoyaltyPoints import LoyaltyPoints

    Customers.transactions = db.relationship("Transactions", back_populates="customer")
    Customers.loyalty_points = db.relationship("LoyaltyPoints", back_populates="customer")

    Transactions.customer = db.relationship("Customers", back_populates="transactions")

    LoyaltyPoints.customer = db.relationship("Customers", back_populates="loyalty_points")

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the db with the app
    db.init_app(app)

    migrate = Migrate(app, db)

    with app.app_context():
        # Initialize models within the application context
        initialize_models()

        # Create the database tables (if they don't exist)
        db.create_all()

    return app
