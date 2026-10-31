import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
num_customers = 1000

# 1. Customers Table
customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
ages = np.random.randint(18, 75, size=num_customers)
genders = np.random.choice(['Male', 'Female'], size=num_customers, p=[0.49, 0.51])
income = np.random.normal(55000, 20000, size=num_customers).astype(int)
income = np.clip(income, 20000, 150000) # Keep within realistic bounds

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'age': ages,
    'gender': genders,
    'annual_income': income
})

# 2. Policies Table
policy_ids = [f"POL{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
policy_types = np.random.choice(['Auto', 'Home', 'Health', 'Life'], size=num_customers, p=[0.4, 0.3, 0.2, 0.1])
tenure_months = np.random.randint(6, 120, size=num_customers)
monthly_premium = np.where(policy_types == 'Health', np.random.randint(150, 400, size=num_customers),
                  np.where(policy_types == 'Home', np.random.randint(100, 300, size=num_customers),
                  np.where(policy_types == 'Auto', np.random.randint(70, 200, size=num_customers), 
                           np.random.randint(50, 150, size=num_customers))))

# Calculate baseline churn risk loosely based on tenure and premium cost
churn_probability = 0.1 + (monthly_premium / 500) - (tenure_months / 240)
churn_probability = np.clip(churn_probability, 0.02, 0.95)
churned = np.random.binomial(1, churn_probability)

df_policies = pd.DataFrame({
    'policy_id': policy_ids,
    'customer_id': customer_ids,
    'policy_type': policy_types,
    'tenure_months': tenure_months,
    'monthly_premium': monthly_premium,
    'churned': churned
})

# 3. Claims Table (Some customers have no claims, some have multiple)
claim_records = []
claim_id_counter = 1

for cust_id in customer_ids:
    num_claims = np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05])
    for _ in range(num_claims):
        claim_id = f"CLM{str(claim_id_counter).zfill(4)}"
        claim_amount = np.random.exponential(scale=1500) + 100
        # Deductible is lower than claim amount
        deductible = claim_amount * np.random.uniform(0.05, 0.2) 
        
        claim_records.append({
            'claim_id': claim_id,
            'customer_id': cust_id,
            'claim_amount': round(claim_amount, 2),
            'deductible': round(deductible, 2)
        })
        claim_id_counter += 1

df_claims = pd.DataFrame(claim_records)

# Save to CSV files so you have them backed up
df_customers.to_csv('customers.csv', index=False)
df_policies.to_csv('policies.csv', index=False)
df_claims.to_csv('claims.csv', index=False)

print("✅ Step 0 Successful: 'customers.csv', 'policies.csv', and 'claims.csv' have been generated!")
