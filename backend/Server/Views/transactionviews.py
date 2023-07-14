from flask_restful import Resource
from flask import request
from app import db
from Server.Models.Transactions import Transactions



class GetAllTransactions(Resource):
    def get(self):
        transactions = Transactions.query.all()
        transaction_list = [{
            "id": transaction.id,
            "customer_id": transaction.customer_id,
            "amount": transaction.amount,
            "transaction_date": transaction.transaction_date
        } for transaction in transactions]

        return {'transactions': transaction_list}, 200


class AddTransaction(Resource):
    def post(self):
        data = request.get_json()
        customer_id = data.get('customer_id')
        amount = data.get('amount')

        if not customer_id or not amount:
            return {'error': 'Invalid data. Please provide customer_id and amount.'}, 400
        
        new_transaction = Transactions(customer_id=customer_id, amount=amount)
        db.session.add(new_transaction)
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
                "transaction_date": transaction.transaction_date
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
        db.session.commit()

        return {'message': 'Transaction updated successfully'}, 200

    def delete(self, transaction_id):
        transaction = Transactions.query.get(transaction_id)
        if not transaction:
            return {"error": "Transaction not found"}, 404

        db.session.delete(transaction)
        db.session.commit()

        return {'message': 'Transaction deleted successfully'}, 200