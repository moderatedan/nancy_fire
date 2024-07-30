import tkinter as tk
from tkinter import messagebox
import os

# Create the main application window
root = tk.Tk()
root.title("My Stock Portfolio")

# Load the image
image_path = "8b8YFRSSshx4Sfy9fk9w--1--0j7p9.png"
if os.path.exists(image_path):
    image = tk.PhotoImage(file=image_path)
    
    # Create a frame to hold the image
    image_frame = tk.Frame(root)
    image_frame.pack()

    # Display the image on the frame
    label = tk.Label(image_frame, image=image)
    label.pack()
else:
    messagebox.showerror("Error", f"Image file not found: {image_path}")

# Run the Tkinter event loop
root.mainloop()