import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
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

# Function to update the displayed data
def update_displayed_data():
    # Fetch the stock transactions
    transactions = fetch_stock_transactions()

    # Clear existing data in the treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Insert the new transactions into the treeview
    for transaction in transactions:
        treeview.insert("", "end", values=list(transaction.values()))

# Create Tkinter window
root = tk.Tk()
root.title("Nancy Pelosi Stock Tracker")

# Create treeview to display financial data
treeview = ttk.Treeview(root, columns=["Date", "Transaction Type"], show="headings", height=20)
treeview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Add column headings
treeview.heading("Date", text="Date")
treeview.heading("Transaction Type", text="Transaction Type")

# Load and display the image using PIL
image_path = "8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png"
if os.path.exists(image_path):
    image = Image.open(image_path)
    image = image.resize((300, 300))  # Resize the image if necessary
    image = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(root, image=image)
    image_label.grid(row=0, column=1, rowspan=2, padx=20, pady=20)
else:
    messagebox.showerror("Error", f"Image file not found: {image_path}")

# Start the Tkinter event loop
root.mainloop()
