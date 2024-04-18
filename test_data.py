import pandas as pd
import numpy as np
from faker import Faker
import random
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Initialize Faker to generate fake data
fake = Faker()

# Generate sample customer data
num_customers = 1000
customer_ids = np.arange(1, num_customers + 1)
customer_names = [fake.name() for _ in range(num_customers)]
age = np.random.randint(18, 70, num_customers)
gender = np.random.choice(['Male', 'Female'], num_customers)
income_level = np.random.choice(['Low', 'Medium', 'High'], num_customers)
education_level = np.random.choice(['High School', 'College', 'Graduate'], num_customers)
marital_status = np.random.choice(['Single', 'Married', 'Divorced'], num_customers)
location = [fake.city() for _ in range(num_customers)]

# Generate sample account data
num_accounts = 500
account_ids = np.arange(1, num_accounts + 1)
account_types = np.random.choice(['Savings', 'Checking', 'Credit Card'], num_accounts)
account_balances = np.random.uniform(100, 10000, num_accounts)
account_open_dates = pd.date_range(start='2022-01-01', end='2022-12-31', periods=num_accounts).tolist()
account_currencies = ['USD' for _ in range(num_accounts)]
account_status = np.random.choice(['Active', 'Closed'], num_accounts)
account_numbers = ['ACCT' + ''.join(random.choices(string.digits, k=8)) for _ in range(num_accounts)]

# Generate sample transaction data
num_transactions = 10000
transaction_ids = np.arange(1, num_transactions + 1)
transaction_dates = pd.date_range(start='2022-01-01', end='2022-12-31', periods=num_transactions).tolist()
transaction_types = np.random.choice(['Deposit', 'Withdrawal', 'Transfer'], num_transactions)
transaction_amounts = np.random.uniform(10, 10000, num_transactions)
merchant_names = [fake.company() for _ in range(num_transactions)]

# Generate sample credit score, loan delinquency, and fraud risk data
credit_scores = np.random.randint(300, 850, num_customers)
loan_delinquency = np.random.choice(['Yes', 'No'], num_customers)
fraud_risk_scores = np.random.randint(1, 100, num_customers)

# Create a DataFrame with the sample data
customer_data = {
    'CustomerID': customer_ids,
    'CustomerName': customer_names,
    'Age': age,
    'Gender': gender,
    'IncomeLevel': income_level,
    'EducationLevel': education_level,
    'MaritalStatus': marital_status,
    'Location': location,
    'CreditScore': credit_scores,
    'LoanDelinquency': loan_delinquency,
    'FraudRiskScore': fraud_risk_scores
}

account_data = {
    'AccountID': account_ids,
    'AccountType': account_types,
    'AccountBalance': account_balances,
    'AccountOpenDate': account_open_dates,
    'AccountCurrency': account_currencies,
    'AccountStatus': account_status,
    'AccountNumber': account_numbers,
    'CustomerID': np.random.choice(customer_ids, num_accounts)
}

transaction_data = {
    'TransactionID': transaction_ids,
    'AccountID': np.random.choice(account_ids, num_transactions),
    'TransactionDate': transaction_dates,
    'TransactionType': transaction_types,
    'TransactionAmount': transaction_amounts,
    'MerchantName': merchant_names
}

customers_df = pd.DataFrame(customer_data)
accounts_df = pd.DataFrame(account_data)
transactions_df = pd.DataFrame(transaction_data)

# Print the first few rows of the DataFrames
print("Customer Data:")
print(customers_df.head())

print("\nAccount Data:")
print(accounts_df.head())

print("\nTransaction Data:")
print(transactions_df.head())
