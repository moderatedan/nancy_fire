import pandas as pd

# Define the transaction data
transaction_data = [
    {"Date": "Feb 21, 2024", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 20, "Underlying": "Palo Alto Networks, Inc. Stock (PANW)", "Strike Price": 200, "Expiration Date": "01/17/2025"},
    {"Date": "Feb 12, 2024", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 50, "Underlying": "Palo Alto Networks, Inc. Stock (PANW)", "Strike Price": 200, "Expiration Date": "01/17/2025"},
    {"Date": "Nov 15, 2023", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 50, "Underlying": "NVIDIA Corporation Stock (NVDA)", "Strike Price": 120, "Expiration Date": "12/20/2024"},
    {"Date": "June 15, 2023", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 50, "Underlying": "Microsoft Corporation (MSFT)", "Strike Price": 180, "Expiration Date": "06/16/2023"},
    {"Date": "June 15, 2023", "Transaction": "Purchase", "Type": "Call Option", "Quantity": 50, "Underlying": "Apple Inc. Stock (AAPL)", "Strike Price": 80, "Expiration Date": "06/16/2023"},
    {"Date": "Mar 17, 2023", "Transaction": "Exercise", "Type": "Call Option", "Quantity": 100, "Underlying": "Apple Inc. Stock (AAPL)", "Strike Price": 80, "Expiration Date": "03/17/2023"},
    {"Date": "Mar 17, 2023", "Transaction": "Loss", "Type": "Quiver Quantitative Data", "Description": "Q4 losses", "Losses": {
        "PayPal stock": 853000,
        "Salesforce options": 733000,
        "Tesla stock": 500000,
        "Roblox options": 235000
    }},
    {"Date": "Mar 09, 2023", "Transaction": "Investment", "Type": "Real Estate", "Description": "Invested in REOF XX LLC, involved in acquiring and restoring a luxury hotel property in San Francisco, CA"},
    {"Date": "Jan 20, 2023", "Transaction": "Loss", "Type": "Call Option", "Quantity": 100, "Underlying": "Roblox Corporation (RBLX)", "Strike Price": 100, "Expiration Date": "01/20/2023", "Total Loss": 303001},
    {"Date": "Dec 30, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "Netflix, Inc. (NFLX)", "Quantity": 1000, "Sale Price": 292.89, "Total Loss": 63535},
    {"Date": "Dec 28, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "SP Alphabet Inc. - Class A (GOOGL)", "Quantity": 10000, "Value Range": "$500,001 to $1,000,000"},
    {"Date": "Dec 28, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "Alliance Bernstein Holding L.P. Units (AB)", "Quantity": 20000, "Sale Price": 32.95, "Total Loss": 11510},
    {"Date": "Dec 28, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "SP PayPal Holdings, Inc. (PYPL)", "Quantity": 5000, "Sale Price": 67.77, "Total Loss": 429938},
    {"Date": "Dec 21, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "SP Alphabet Inc. - Class A (GOOGL)", "Quantity": 10000, "Value Range": "$500,001 to $1,000,000"},
    {"Date": "Dec 21, 2022", "Transaction": "Sale", "Type": "Partial Sale", "Underlying": "Walt Disney Company (DIS)", "Quantity": 10000, "Average Price": 87.58, "Total Loss": 114138, "Value Range": "$500,001 to $1,000,000"},
    {"Date": "Dec 21, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "PayPal Holdings, Inc. (PYPL)", "Quantity": 5000, "Sale Price": 69.10, "Total Loss": 424313},
    {"Date": "Dec 20, 2022", "Transaction": "Sale", "Type": "Call Option", "Quantity": 130, "Underlying": "Salesforce, Inc. (CRM)", "Strike Price": 210, "Expiration Date": "01/20/2023", "Sale Price": 0.01, "Total Loss": 733691},
    {"Date": "Dec 20, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "SP Alphabet Inc. - Class A (GOOGL)", "Quantity": 10000, "Value Range": "$500,001 to $1,000,000"},
    {"Date": "Dec 20, 2022", "Transaction": "Partial Sale", "Type": "Stock", "Underlying": "Tesla, Inc. (TSLA)", "Quantity": 5000, "Average Price": 140.38, "Total Loss": 511197},
    {"Date": "Nov 08, 2022", "Transaction": "Sale", "Type": "Stock", "Underlying": "Visa Inc. (V)", "Quantity": 20000},
    {"Date": "Sept 16, 2022", "Transaction": "Exercise", "Type": "Call Option", "Quantity": 200, "Underlying": "Alphabet Inc. (GOOGL)", "Strike Price": 100, "Expiration Date": "09/16/2022"},
    {"Date": "Sept 16, 2022", "Transaction": "Sale", "Type": "Call Option", "Underlying": "Micron Technology (MU)", "Quantity": 100, "Strike Price": 50, "Expiration Date": "09/16/2022", "Sale Price": 1.84, "Total Loss": 392575},
    {"Date": "Sept 16, 2022", "Transaction": "Sale", "Type": "Call Option", "Underlying": "NVIDIA Corporation (NVDA)", "Quantity": 50
]
