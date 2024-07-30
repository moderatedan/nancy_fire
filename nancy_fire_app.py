import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Function to fetch and parse the stock transaction data
def fetch_stock_transactions():
    url = "https://stockscan.io/nancy-pelosi-stock-tracker"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    transactions = []
    for row in soup.find_all("tr")[1:]:
        cells = row.find_all("td")
        date = cells[0].text.strip()  # Remove leading/trailing whitespaces
        transaction_type = cells[1].text.strip()  # Remove leading/trailing whitespaces
        transactions.append({
            "Date": date,
            "Transaction Type": transaction_type,
        })
    return transactions

# Function to update the displayed stock data
def update_stock_data():
    transactions = fetch_stock_transactions()
    for row in stock_treeview.get_children():
        stock_treeview.delete(row)
    for transaction in transactions:
        stock_treeview.insert("", "end", values=list(transaction.values()))

# Function to display financial data
def display_financial_data():
    # Print to debug CSV loading
    print("Displaying financial data")
    print(transaction_df.head())  # Print the first few rows of the DataFrame

    for row in financial_treeview.get_children():
        financial_treeview.delete(row)
    
    for index, row in transaction_df.iterrows():
        financial_treeview.insert("", "end", values=list(row))
        # Print each row being inserted
        print(list(row))

# Function to analyze transactions and plot data
def analyze_transactions():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(transaction_df['Quantity'], bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Distribution of Transaction Quantities')
    ax.set_xlabel('Quantity')
    ax.set_ylabel('Frequency')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=analyze_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Main application window
root = tk.Tk()
root.title("Nancy Fire Projects")

# Create tabs
tab_control = ttk.Notebook(root)

# Tab 1: Image Display
image_tab = ttk.Frame(tab_control)
tab_control.add(image_tab, text='Image Display')

image_path = "8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png"
if os.path.exists(image_path):
    image = tk.PhotoImage(file=image_path)
    label = tk.Label(image_tab, image=image)
    label.pack()
else:
    tk.messagebox.showerror("Error", f"Image file not found: {image_path}")

# Tab 2: Financial Data Viewer
financial_tab = ttk.Frame(tab_control)
tab_control.add(financial_tab, text='Financial Data Viewer')

csv_path = 'transaction_data.csv'
if os.path.exists(csv_path):
    transaction_df = pd.read_csv(csv_path)
    # Print to debug CSV loading
    print("CSV loaded successfully")
    print(transaction_df.head())  # Print the first few rows of the DataFrame
else:
    tk.messagebox.showerror("Error", f"CSV file not found: {csv_path}")
    transaction_df = pd.DataFrame()

financial_treeview = ttk.Treeview(financial_tab, columns=list(transaction_df.columns), show="headings", height=20)
financial_treeview.pack(expand=True, fill='both')

for col in transaction_df.columns:
    financial_treeview.heading(col, text=col)

display_financial_data_button = ttk.Button(financial_tab, text="Refresh", command=display_financial_data)
display_financial_data_button.pack()

# Tab 3: Transaction Analyzer
analyze_tab = ttk.Frame(tab_control)
tab_control.add(analyze_tab, text='Transaction Analyzer')

analyze_frame = tk.Frame(analyze_tab)
analyze_frame.pack(expand=True, fill='both')

analyze_button = ttk.Button(analyze_tab, text="Analyze Transactions", command=analyze_transactions)
analyze_button.pack()

# Tab 4: Stock Tracker
stock_tab = ttk.Frame(tab_control)
tab_control.add(stock_tab, text='Stock Tracker')

stock_treeview = ttk.Treeview(stock_tab, columns=["Date", "Transaction Type"], show="headings", height=20)
stock_treeview.pack(expand=True, fill='both')

stock_treeview.heading("Date", text="Date")
stock_treeview.heading("Transaction Type", text="Transaction Type")

update_stock_data_button = ttk.Button(stock_tab, text="Update Data", command=update_stock_data)
update_stock_data_button.pack()

update_stock_data()

tab_control.pack(expand=True, fill='both')

# Start the Tkinter event loop
root.mainloop()
