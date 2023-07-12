from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
from app import db 



class Customers(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    phone_number = db.Column(db.Integer(15), nullable=False)

    @validates('name')
    def validate_username(self, key, name):
        assert len(name) >= 8, "name must be at least 8 characters long."
        return name

    @validates('email')
    def validate_email(self, key, email):
            assert '@' in email, "Email address must contain the @ symbol."
            assert '.' in email.split('@')[-1], "Email address must have a valid domain name."
            return email
    
    def __repr__(self):
        return f"User(id={self.id}, username='{self.name}', email='{self.email}', phone = {self.phone_number})"