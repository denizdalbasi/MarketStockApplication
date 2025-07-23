# Main application entry point
import tkinter as tk
# Import the MarketStockApplication class from the MarketStockApp module
from MarketStockApplication import MarketStockApplication

# This block ensures the code runs only when the script is executed directly
if __name__ == "__main__":
    # Create the main Tkinter window (root window)
    root = tk.Tk()
    # Create an instance of the MarketStockApplication, passing the root window
    application = MarketStockApplication(root)
    # Start the Tkinter event loop, which keeps the application running
    root.mainloop()