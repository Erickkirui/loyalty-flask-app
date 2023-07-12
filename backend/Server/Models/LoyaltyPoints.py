from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
from app import db
#from Customers import Customers

class LoyaltyPoints(db.Model):
    __tablename__ = 'loyaltypoints'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    points = db.Column(db.Integer, nullable=False)

    customer = db.relationship("Customers", back_populates="loyaltypoints")

def __repr__(self):
        return f"customer_id={self.customer_id}, points={self.points})"