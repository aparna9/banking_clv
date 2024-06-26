import numpy as np
import pytz
import psycopg2 

from psycopg2 import sql
from faker import Faker
from flask import Flask, jsonify, request
from datetime import datetime,timezone,timedelta
from azure.identity import ClientSecretCredential,ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# assign values 
# AZURE_CLIENT_ID = "6a394ed0-8825-44b2-baf5-acf94e95c705"
# AZURE_TENANT_ID = "056e6750-b527-40b5-bc55-1d8da5c3ffe4"
# AZURE_CLIENT_SECRET = "pnf8Q~xLMSfmZlWSGs0EDbpKrT3FLzayQYpUdc_G"
AZURE_VAULT_URL = "https://bankingclvdbcreds.vault.azure.net"
secret_name = "BANKINGCLV-DBPASSWORD"

# create credential 

# credentials = ClientSecretCredential(
# AZURE_TENANT_ID,AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
# )

credentials = ManagedIdentityCredential()
client = SecretClient(vault_url=AZURE_VAULT_URL,credential=credentials)

#create secrent client object 

secret_client = SecretClient(vault_url=AZURE_VAULT_URL, credential=credentials)

# retrieve secret value

secret = secret_client.get_secret(secret_name).value

#  Connecting to database

try:
    cnx = psycopg2.connect(
        user="bankingclvdb", password=secret, 
        host="bankingclvpg.postgres.database.azure.com", port=5432, database="banking_clv") 
except Exception as e:
    print(f"Connection Error : {e}")

# get all the existing customers 

cur = cnx.cursor()
cur.execute("select distinct cust_id from public.bnk_customer;")
result = cur.fetchall()
# print(f"sql result : {result}")


app = Flask(__name__)
fake = Faker()

# Set seed for reproducibility
np.random.seed(42)

def generate_new_customers(exclude_customers , start = 1 , end = 1000000):
    while True:
        customer_id = np.random.randint(start, end)
        if customer_id not in exclude_customers:
            return customer_id



def generate_data():
    # Generate synthetic customer data
    customers = [{
        # 'CustomerID': int(np.random.randint(1, 1000000)),
        'CustomerID': generate_new_customers(result),
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
            account_id = int(np.random.randint(1, 1000000))
            account_type = fake.random_element(['Savings', 'Checking', 'Credit Card'])
            account_balance = float(np.random.uniform(0, 100000))
            open_date = fake.date_time_between(start_date='-5y', end_date='now') # Open date within the last 5 years
            close_date = open_date + timedelta(days=np.random.randint(1, 365)) # Close date within 1 year of open date
            close_date = close_date if np.random.random() < 0.2 else None  # 20% chance of account being closed

            open_date_str = open_date.strftime('%Y-%m-%d') if open_date is not None else None
            close_date_str = close_date.strftime('%Y-%m-%d') if close_date is not None else None

            accounts.append({
                'AccountID': account_id,
                'CustomerID': customer['CustomerID'],
                'AccountBalance': account_balance,
                'AccountType': account_type,
                'OpenDate': open_date_str,
                'CloseDate' : close_date_str
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

def generate_ct_time():
    utc_now = datetime.now(timezone.utc)
    tz = pytz.timezone('America/Chicago')
    central_now = utc_now.astimezone(tz)

    return central_now

@app.route('/api/data', methods=['POST'])
def update_data():
    global customers, accounts, transactions
    customers, accounts, transactions = generate_data()

    current_datetime = generate_ct_time().strftime('%Y-%m-%d %H:%M:%S') 
    metadata = {'generated_at': current_datetime}
    return jsonify({'message': 'Data refreshed successfully', 'metadata': metadata})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    global customers

    current_datetime = generate_ct_time().strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'total_records': len(customers), 'generated_at': current_datetime}
    return jsonify({'data': customers, 'metadata': metadata})

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    global accounts

    current_datetime = generate_ct_time().strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'total_records': len(accounts), 'generated_at': current_datetime}
    return jsonify({'data': accounts, 'metadata': metadata})

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    global transactions

    current_datetime = generate_ct_time().strftime('%Y-%m-%d %H:%M:%S')
    metadata = {'total_records': len(transactions), 'generated_at': current_datetime}
    return jsonify({'data': transactions, 'metadata': metadata})

if __name__ == '__main__':
    customers, accounts, transactions = generate_data()
    app.run(debug=True)
