import json
import numpy as np
import pytz
from faker import Faker
from flask import Flask, jsonify, request
from datetime import datetime,timezone

app = Flask(__name__)
fake = Faker()

# Set seed for reproducibility
np.random.seed(42)

def generate_data():
    # Generate synthetic customer data
    customers = [{
        'CustomerID': int(np.random.randint(1, 1000000)),
        'CustomerName': fake.name(),
        'Age': int(np.random.randint(18, 80)),
        'Gender': fake.random_element(['Male', 'Female']),
        'Income': float(np.random.uniform(20000, 150000)),
        'Address': fake.address().replace("\n", ", "),
        'JoinDate': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
    } for _ in range(100)]

    # Generate synthetic account data
    accounts = []
    for customer in customers:
        num_accounts = np.random.randint(1, 4)
        for _ in range(num_accounts):
            accounts.append({
                'AccountID': int(np.random.randint(1, 1000000)),
                'CustomerID': customer['CustomerID'],
                'AccountBalance': float(np.random.uniform(0, 100000)),
                'AccountType': fake.random_element(['Savings', 'Checking', 'Credit Card'])
            })

    # Generate synthetic transaction data
    transactions = []
    for account in accounts:
        num_transactions = np.random.randint(1, 11)
        for _ in range(num_transactions):
            transactions.append({
                'TransactionID': int(np.random.randint(1, 1000000)),
                'AccountID': account['AccountID'],
                'TransactionAmount': float(np.random.uniform(-5000, 5000)),
                'TransactionType': fake.random_element(['Deposit', 'Withdrawal', 'Transfer']),
                'TransactionDate': fake.date_this_year()
            })

    return customers, accounts, transactions

@app.route('/api/data', methods=['POST'])
def update_data():
    global customers, accounts, transactions
    customers, accounts, transactions = generate_data()

    utc_now = datetime.now(timezone.utc)
    tz = pytz.timezone('America/Chicago')
    central_now = utc_now.astimezone(tz)

    current_datetime = central_now.strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'generated_at': current_datetime}
    return jsonify({'message': 'Data refreshed successfully', 'metadata': metadata})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    global customers

    utc_now = datetime.now(timezone.utc)
    tz = pytz.timezone('America/Chicago')
    central_now = utc_now.astimezone(tz)

    current_datetime = central_now.strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'total_records': len(customers), 'generated_at': current_datetime}
    return jsonify({'data': customers, 'metadata': metadata})

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    global accounts
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'total_records': len(accounts), 'generated_at': current_datetime}
    return jsonify({'data': accounts, 'metadata': metadata})

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    global transactions
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'total_records': len(transactions), 'generated_at': current_datetime}
    return jsonify({'data': transactions, 'metadata': metadata})

if __name__ == '__main__':
    customers, accounts, transactions = generate_data()
    app.run(debug=True)
