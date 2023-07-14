from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin

from app import db
#from Customers import Customers

class Transactions(db.Model,SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    amount = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime,server_default=db.func.now() )

    customer = db.relationship('Customers', back_populates='transactions')

def __repr__(self):
        return f"Transaction(id={self.id}, customer_id={self.customer_id}, amount={self.amount}, transaction_date={self.transaction_date})"