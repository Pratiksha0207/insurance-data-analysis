import sqlite3
import pandas as pd
import os

print("⏳ Setting up SQL Database and running queries...")

# Load our newly generated CSV files
df_cust = pd.read_csv('customers.csv')
df_pol = pd.read_csv('policies.csv')
df_clm = pd.read_csv('claims.csv')

# Create a temporary in-memory SQL database
conn = sqlite3.connect(':memory:')

# Push the dataframes into SQL Tables
df_cust.to_sql('Customers', conn, index=False, if_exists='replace')
df_pol.to_sql('Policies', conn, index=False, if_exists='replace')
df_clm.to_sql('Claims', conn, index=False, if_exists='replace')

# 📝 INTERMEDIATE SQL QUERY
# Uses a CTE to group claims, JOINS all 3 tables, and calculates a revenue metric using a Window Function
sql_query = """
WITH CustomerClaims AS (
    SELECT 
        customer_id,
        COUNT(claim_id) as total_claims,
        SUM(claim_amount) as total_claim_amount,
        SUM(deductible) as total_deductible_paid
    FROM Claims
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.age,
    c.gender,
    c.annual_income,
    p.policy_id,
    p.policy_type,
    p.tenure_months,
    p.monthly_premium,
    p.churned,
    COALESCE(cc.total_claims, 0) as total_claims,
    COALESCE(cc.total_claim_amount, 0) as total_claim_amount,
    COALESCE(cc.total_deductible_paid, 0) as total_deductible_paid,
    -- Window Function: Calculate cumulative total premiums collected across the portfolio per insurance type
    SUM(p.monthly_premium * p.tenure_months) OVER(PARTITION BY p.policy_type) as running_total_segment_revenue
FROM Customers c
JOIN Policies p ON c.customer_id = p.customer_id
LEFT JOIN CustomerClaims cc ON c.customer_id = cc.customer_id;
"""

# Run query and save to a dataframe
df_master = pd.read_sql_query(sql_query, conn)
conn.close()

# Export the SQL output to a new CSV file
df_master.to_csv('insurance_sql_output.csv', index=False)
print("✅ Step 1 Successful: SQL Query executed! Data joined and saved to 'insurance_sql_output.csv'.")
print("\n--- Preview of SQL Output ---")
print(df_master.head(3))
