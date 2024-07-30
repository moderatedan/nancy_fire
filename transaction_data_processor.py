import pandas as pd
import os

# Define the transaction data
transaction_data = [
    {"Date": "Feb 21, 2024", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 20, "Underlying": "Palo Alto Networks, Inc. Stock (PANW)", "Strike Price": 200, "Expiration Date": "01/17/2025"},
    {"Date": "Feb 12, 2024", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 50, "Underlying": "Palo Alto Networks, Inc. Stock (PANW)", "Strike Price": 200, "Expiration Date": "01/17/2025"},
    {"Date": "Nov 15, 2023", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 50, "Underlying": "NVIDIA Corporation Stock (NVDA)", "Strike Price": 120, "Expiration Date": "12/20/2024"},
    # Rest of the transaction data...
]

# Convert the dates to datetime format
for transaction in transaction_data:
    transaction["Date"] = pd.to_datetime(transaction["Date"], format="%b %d, %Y")

# Convert the transaction data into a DataFrame
transaction_df = pd.DataFrame(transaction_data)

# Save the DataFrame as a CSV file
csv_path = 'transaction_data.csv'
transaction_df.to_csv(csv_path, index=False)

print("CSV file saved successfully.")
