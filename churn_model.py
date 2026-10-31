import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

print("⏳ Running Advanced Python Machine Learning Model...")

# 1. Load the SQL consolidated dataset
if not os.path.exists('insurance_sql_output.csv'):
    raise FileNotFoundError("Please run sql_analysis.py first to generate the master dataset!")

df = pd.read_csv('insurance_sql_output.csv')

# 2. Advanced Feature Engineering & Data Prep
# Convert text columns (Gender and Policy Type) into numbers so the AI can read them
le_gender = LabelEncoder()
df['gender_encoded'] = le_gender.fit_transform(df['gender'])

le_type = LabelEncoder()
df['policy_type_encoded'] = le_type.fit_transform(df['policy_type'])

# Select the features (inputs) the AI will use to learn patterns
feature_cols = ['age', 'gender_encoded', 'annual_income', 'policy_type_encoded', 
                'tenure_months', 'monthly_premium', 'total_claims', 'total_claim_amount']

X = df[feature_cols]
y = df['churned'] # The target we want to predict (1 = Left, 0 = Stayed)

# Split data: 80% to train the AI, 20% to test how smart it is
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Model Training (Random Forest Classifier)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate model accuracy
accuracy = model.score(X_test, y_test)
print(f"🎯 Model Training Complete. Test Accuracy: {accuracy * 100:.2f}%")

# 4. Generate Predictions & Risk Scores for ALL Customers
# predict_proba gives the percentage chance of churning
df['churn_risk_score'] = (model.predict_proba(X)[:, 1] * 100).round(2)

# Categorise customers based on their risk score
df['risk_segment'] = np.where(df['churn_risk_score'] > 70, 'High Risk',
                     np.where(df['churn_risk_score'] > 35, 'Medium Risk', 'Low Risk'))

# 5. Save the final AI-analyzed dataset for Excel and Power BI
df.to_csv('insurance_final_predictions.csv', index=False)
print("✅ Step 2 Successful: Machine Learning predictions saved to 'insurance_final_predictions.csv'!")
print("\n--- Top 3 Highest Risk Customers Identified ---")
print(df[df['risk_segment'] == 'High Risk'][['customer_id', 'policy_type', 'churn_risk_score', 'risk_segment']].head(3))
