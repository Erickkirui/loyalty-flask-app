from flask_restful import Resource
from Server.Models.Customers import Customers
from flask import request
from app import db


# api request for customers

class GetAllCustomers(Resource):
    def get(self):
        customers = Customers.query.all()
        customer_list = [{
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone_number": customer.phone_number
        } for customer in customers]

        return {'customers': customer_list}, 200
    
class AddCustomer(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if not name or not email or not phone_number:
            return {'error': 'Invalid data. Please provide name, email, and phone number.'}, 400

        new_customer = Customers(name=name, email=email, phone_number=phone_number)
        db.session.add(new_customer)
        db.session.commit()
        
        return {'message': 'New user created successfully'}, 201
    
class CustomerResourcesById(Resource):
    def get(self, customer_id):
        customer = Customers.query.get(customer_id)
        if customer:
            return {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone_number": customer.phone_number
            }, 200
        else:
            return {"error": "Customer not found"}, 404

    def delete(self, customer_id):
        customer = Customers.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return {"message": "Customer deleted successfully"}, 200
        else:
            return {"error": "Customer not found"}, 404

    def patch(self, customer_id):
        customer = Customers.query.get(customer_id)
        if not customer:
            return {"error": "Customer not found"}, 404

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if name:
            customer.name = name
        if email:
            customer.email = email
        if phone_number:
            customer.phone_number = phone_number

        db.session.commit()

        return {"message": "Customer updated successfully"}, 200