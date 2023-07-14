# import random
# from datetime import datetime, timedelta
# from app import create_app, db
# from Server.Models.Customers import Customers
# from Server.Models.Transactions import Transactions
# from Server.Models.LoyaltyPoints import LoyaltyPoints

# app = create_app('config')  # Update with your actual config name
# app.app_context().push()

# # Helper function to generate random phone numbers
# def generate_phone_number():
#     return random.randint(1000000000, 9999999999)

# # Helper function to generate random transaction dates
# def generate_transaction_date():
#     now = datetime.now()
#     random_days = random.randint(1, 30)
#     return now - timedelta(days=random_days)

# # Generate random customers
# def generate_customers(num_customers):
#     customers = []
#     for _ in range(num_customers):
#         name = "Customer" + str(random.randint(1, 100))
#         email = name.lower() + "@example.com"
#         phone_number = generate_phone_number()
#         customer = Customers(name=name, email=email, phone_number=phone_number)
#         customers.append(customer)
#     return customers

# # Generate random transactions for each customer
# def generate_transactions(customers):
#     transactions = []
#     for customer in customers:
#         num_transactions = random.randint(1, 5)
#         for _ in range(num_transactions):
#             amount = random.randint(10, 100)
#             transaction_date = generate_transaction_date()
#             transaction = Transactions(customer=customer, amount=amount, transaction_date=transaction_date)
#             transactions.append(transaction)
#     return transactions

# # Generate random loyalty points for each customer
# def generate_loyalty_points(customers):
#     loyalty_points = []
#     for customer in customers:
#         points = random.randint(0, 100)
#         loyalty_point = LoyaltyPoints(customer=customer, points=points)
#         loyalty_points.append(loyalty_point)
#     return loyalty_points

# # Populate the tables with random data
# def seed_data():
#     num_customers = 10  # Update with the desired number of customers

#     customers = generate_customers(num_customers)
#     transactions = generate_transactions(customers)
#     loyalty_points = generate_loyalty_points(customers)

#     db.session.bulk_save_objects(customers)
#     db.session.bulk_save_objects(transactions)
#     db.session.bulk_save_objects(loyalty_points)
#     db.session.commit()

# if __name__ == '__main__':
#     seed_data()
