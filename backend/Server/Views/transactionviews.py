from flask_restful import Resource
from flask import request
from app import db
from Server.Models.Transactions import Transactions
from Server.Models.Customers import Customers
from Server.Models.LoyaltyPoints import LoyaltyPoints
from datetime import datetime
from sqlalchemy import func



class GetAllTransactions(Resource):
    def get(self):
        transactions = Transactions.query.all()
        transaction_list = [{
            "id": transaction.id,
            "customer_id": transaction.customer_id,
            "amount": transaction.amount,
            "transaction_date": transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S")  # Format the datetime as a string
        } for transaction in transactions]

        return {'transactions': transaction_list}, 200



class AddTransaction(Resource):
    def post(self):
        data = request.get_json()
        customer_id = data.get('customer_id')
        amount = data.get('amount')

        if not customer_id or not amount:
            return {'error': 'Invalid data. Please provide customer_id and amount.'}, 400

        # Check if the customer exists
        customer = Customers.query.get(customer_id)
        if not customer:
            return {'error': 'Invalid customer_id. Customer not found.'}, 404

        # Check if the customer already has a transaction
        existing_transaction = Transactions.query.filter_by(customer_id=customer_id).first()

        try:
            amount = int(amount)
        except ValueError:
            return {'error': 'Invalid amount. Amount must be an integer.'}, 400

        if existing_transaction:
            existing_transaction.amount += amount

            # Update loyalty points
            loyalty_points = LoyaltyPoints.query.filter_by(customer_id=customer_id).first()
            if loyalty_points:
                loyalty_points.points = int(existing_transaction.amount / 100)
            else:
                loyalty_points = LoyaltyPoints(customer_id=customer_id, points=int(existing_transaction.amount / 100))
                db.session.add(loyalty_points)

            db.session.commit()
            return {'message': 'Transaction amount updated successfully'}, 200
        else:
            new_transaction = Transactions(customer_id=customer_id, amount=amount)
            db.session.add(new_transaction)
            db.session.commit()

            # Update loyalty points
            loyalty_points = LoyaltyPoints.query.filter_by(customer_id=customer_id).first()
            if loyalty_points:
                loyalty_points.points = int(amount / 100)
            else:
                loyalty_points = LoyaltyPoints(customer_id=customer_id, points=int(amount / 100))
                db.session.add(loyalty_points)

            db.session.commit()

            return {'message': 'New transaction created successfully'}, 201



class TransactionResource(Resource):
    def get(self, transaction_id):
        transaction = Transactions.query.get(transaction_id)
        if transaction:
            return {
                "id": transaction.id,
                "customer_id": transaction.customer_id,
                "amount": transaction.amount,
                "transaction_date": transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": transaction.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }, 200
        else:
            return {"error": "Transaction not found"}, 404

    def patch(self, transaction_id):
        transaction = Transactions.query.get(transaction_id)
        if not transaction:
            return {"error": "Transaction not found"}, 404

        data = request.get_json()
        amount = data.get('amount')

        if not amount:
            return {'error': 'Invalid data. Please provide amount.'}, 400

        transaction.amount = amount
        transaction.transaction_date = datetime.now()  # Update the transaction_date to the current time
        db.session.commit()

        # should be moved to loyalty points endpoints
        
        #  # Get the customer ID
        # customer_id = transaction.customer_id

        # # Update the transaction amount
        # transaction.amount = amount
        # db.session.commit()

        # # Update loyalty points
        # loyalty_points = LoyaltyPoints.query.filter_by(customer_id=customer_id).first()
        # if loyalty_points:
        #     loyalty_points.points = int(amount / 100)
        # else:
        #     loyalty_points = LoyaltyPoints(customer_id=customer_id, points=int(amount / 100))
        #     db.session.add(loyalty_points)
        # db.session.commit()

        return {'message': 'Transaction updated successfully', 'transaction_date': transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S")}, 200

    def delete(self, transaction_id):
        transaction = Transactions.query.get(transaction_id)
        if not transaction:
            return {"error": "Transaction not found"}, 404
        
        # Get the customer ID
        customer_id = transaction.customer_id

        db.session.delete(transaction)
        db.session.commit()

        # Update loyalty points
        total_amount = db.session.query(func.sum(Transactions.amount)).filter_by(customer_id=customer_id).scalar()
        total_points = int(total_amount / 100) if total_amount else 0

        loyalty_points = LoyaltyPoints.query.filter_by(customer_id=customer_id).first()
        if loyalty_points:
            loyalty_points.points = total_points
        db.session.commit()

        return {'message': 'Transaction deleted successfully'}, 200
