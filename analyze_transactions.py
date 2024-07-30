import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV file path (relative to the script location)
csv_path = 'transaction_data.csv'

# Check if the CSV file exists
if os.path.exists(csv_path):
    # Load the CSV file into a DataFrame
    transaction_df = pd.read_csv(csv_path)

    # Display the first few rows of the DataFrame
    print("First few rows of the DataFrame:")
    print(transaction_df.head())

    # Perform basic data analysis
    print("\nSummary statistics of numerical columns:")
    print(transaction_df.describe())

    # Plot a histogram of transaction quantities
    plt.figure(figsize=(8, 6))
    plt.hist(transaction_df['Quantity'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Transaction Quantities')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
else:
    print(f"CSV file not found: {csv_path}")
