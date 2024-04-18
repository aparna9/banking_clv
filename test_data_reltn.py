import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()

# Define the number of rows for each dataframe
num_customers = 100
num_accounts = 200
num_transactions = 1000

# Generate customer data
customer_data = []
for i in range(num_customers):
    customer_data.append({
        'customer_id': i + 1,
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'age': np.random.randint(18, 65),
        'gender': np.random.choice(['Male', 'Female'])
    })
customers_df = pd.DataFrame(customer_data)

# Generate account data
account_data = []
for i in range(num_accounts):
    account_data.append({
        'account_id': i + 1,
        'customer_id': np.random.randint(1, num_customers + 1),
        'account_type': np.random.choice(['Checking', 'Savings']),
        'balance': np.random.uniform(100, 10000)
    })
accounts_df = pd.DataFrame(account_data)

# Generate transaction data
transaction_data = []
for i in range(num_transactions):
    transaction_data.append({
        'transaction_id': i + 1,
        'account_id': np.random.randint(1, num_accounts + 1),
        'transaction_type': np.random.choice(['Deposit', 'Withdrawal']),
        'amount': np.random.uniform(1, 1000),
        'date': fake.date_time_this_year()
    })
transactions_df = pd.DataFrame(transaction_data)

# Create relationships between dataframes
transactions_df = pd.merge(transactions_df, accounts_df, on='account_id')
accounts_df = pd.merge(accounts_df, customers_df, on='customer_id')

# Display the first few rows of each dataframe
print("Customers:")
print(customers_df.head())
print("\nAccounts:")
print(accounts_df.head())
print("\nTransactions:")
print(transactions_df.head())
