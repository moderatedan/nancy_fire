import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# CSV file path (relative to the script location)
csv_path = 'transaction_data.csv'

# Check if the CSV file exists
if os.path.exists(csv_path):
    # Read financial data from CSV file
    transaction_df = pd.read_csv(csv_path)
else:
    messagebox.showerror("Error", f"CSV file not found: {csv_path}")
    transaction_df = pd.DataFrame()  # Create an empty DataFrame

def display_financial_data():
    # Clear any existing data in the treeview
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Insert financial data into the treeview
    for index, row in transaction_df.iterrows():
        treeview.insert("", "end", values=list(row))

# Create Tkinter window
root = tk.Tk()
root.title("Financial Data Viewer")

# Load the image
image_path = "8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png"
if os.path.exists(image_path):
    image = tk.PhotoImage(file=image_path)
    
    # Create a label to display the image
    image_label = tk.Label(root, image=image)
    image_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
else:
    messagebox.showerror("Error", f"Image file not found: {image_path}")

# Create treeview to display financial data
treeview = ttk.Treeview(root, columns=list(transaction_df.columns), show="headings", height=20)
treeview.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# Add column headings
for col in transaction_df.columns:
    treeview.heading(col, text=col)

# Create a button to refresh and display financial data
refresh_button = ttk.Button(root, text="Refresh", command=display_financial_data)
refresh_button.grid(row=1, column=1, pady=10)

# Initial display of financial data
if not transaction_df.empty:
    display_financial_data()

# Configure row and column resizing behavior
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the Tkinter event loop
root.mainloop()
