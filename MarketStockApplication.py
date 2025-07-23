import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
# Import the Product class from the Product module
from Product import Product


class MarketStockApplication:
    """
    A Tkinter-based application for managing market stock.
    Allows adding, deleting, updating product stock, and saving/loading data.
    """
    def __init__(self, root):
        """
        Initializes the MarketStockApplication.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Market Stock Program")  # Set the window title
        self.root.geometry("800x600")  # Set the initial window size

        self.products = []  # List to store Product objects
        self.file_name = "stock_data.txt"  # File to store product data

        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=0)  # Toolbar row, fixed size
        self.root.grid_rowconfigure(1, weight=1)  # Table row, expands vertically
        self.root.grid_rowconfigure(2, weight=0)  # Status bar row, fixed size
        self.root.grid_columnconfigure(0, weight=1)  # Main column, expands horizontally
        self.root.grid_columnconfigure(1, weight=0)  # Scrollbar column, fixed size

        # Initialize UI components
        self.create_toolbar()
        self.create_product_list_table()
        self.create_status_bar()

        # Load existing product data when the application starts
        self.load_products()

    def create_toolbar(self):
        """
        Creates the toolbar frame with buttons for various actions.
        """
        toolbar = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        # Place the toolbar at the top, spanning both columns and expanding horizontally
        toolbar.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

        # Button to add a new product
        btn_add_product = tk.Button(toolbar, text="Add Product", command=self.add_product)
        btn_add_product.grid(row=0, column=0, padx=5, pady=2)

        # Button to delete the selected product
        btn_delete_product = tk.Button(toolbar, text="Delete Selected Product", command=self.delete_product)
        btn_delete_product.grid(row=0, column=1, padx=5, pady=2)

        # Button to update the stock quantity of a selected product
        btn_update_stock = tk.Button(toolbar, text="Update Stock", command=self.update_stock)
        btn_update_stock.grid(row=0, column=2, padx=5, pady=2)

        # Button to save all current product data to the file
        btn_save_data = tk.Button(toolbar, text="Save Data", command=self.save_products)
        btn_save_data.grid(row=0, column=3, padx=5, pady=2)

        # Button to exit the application
        btn_exit = tk.Button(toolbar, text="Exit", command=self.root.destroy)
        btn_exit.grid(row=0, column=4, padx=5, pady=2)

        # Configure columns in the toolbar to expand equally
        for i in range(5):
            toolbar.grid_columnconfigure(i, weight=1)

    def create_product_list_table(self):
        """
        Creates the Treeview widget to display the list of products.
        """
        self.tree = ttk.Treeview(self.root, columns=("name", "price", "price_with_vat", "quantity", "min_quantity"), show="headings")

        # Place the Treeview in the main content area, expanding in all directions
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Define column headings
        self.tree.heading("name", text="Product Name")
        self.tree.heading("price", text="Price (TL)")
        self.tree.heading("price_with_vat", text="Price with VAT (TL)")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("min_quantity", text="Min Quantity")

        # Define column widths and alignment
        self.tree.column("name", width=150)
        self.tree.column("price", width=100, anchor=tk.E)  # Align price to the right
        self.tree.column("price_with_vat", width=120, anchor=tk.E)  # Align price with VAT to the right
        self.tree.column("quantity", width=80, anchor=tk.E)  # Align quantity to the right
        self.tree.column("min_quantity", width=100, anchor=tk.E)  # Align min quantity to the right

        # Add a vertical scrollbar to the Treeview
        vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns")  # Place scrollbar next to the table
        self.tree.configure(yscrollcommand=vsb.set)  # Link scrollbar to Treeview

        # Bind a click event to the Treeview to show selected product details in the status bar
        self.tree.bind("<ButtonRelease-1>", self.show_selected_product_details)

    def create_status_bar(self):
        """
        Creates the status bar at the bottom of the window to display messages.
        """
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        # Place the status bar at the bottom, spanning both columns and expanding horizontally
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", ipady=2)

    def add_product(self):
        """
        Prompts the user for product details and adds a new product to the list.
        Performs input validation.
        """
        name = simpledialog.askstring("Add Product", "Product Name:")
        if not name:  # If user cancels or enters empty string
            return

        try:
            price = simpledialog.askfloat("Add Product", f"Price for {name} (TL):")
            if price is None:  # If user cancels
                return
            if price <= 0:
                messagebox.showerror("Error", "Price must be a positive number.")
                return

            quantity = simpledialog.askinteger("Add Product", f"Quantity for {name}:")
            if quantity is None:  # If user cancels
                return
            if quantity < 0:
                messagebox.showerror("Error", "Quantity cannot be negative.")
                return

            min_quantity = simpledialog.askinteger("Add Product", f"Minimum Quantity for {name}:")
            if min_quantity is None:  # If user cancels
                return
            if min_quantity < 0:
                messagebox.showerror("Error", "Minimum quantity cannot be negative.")
                return
            if min_quantity > quantity:
                messagebox.showwarning("Warning", "Minimum quantity cannot be more than current quantity.")
                # Allow adding but warn the user

            # Create a new Product object
            new_product = Product(name, price, quantity, min_quantity)
            self.products.append(new_product)  # Add product to the list
            self.refresh_product_list()  # Update the Treeview display
            self.status_bar.config(text=f"'{name}' product added.")  # Update status bar
            self.save_products()  # Save changes to file
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for price, quantity, and min quantity.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def delete_product(self):
        """
        Deletes the selected product(s) from the list after user confirmation.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return

        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected product(s)?")
        if confirmation:
            # Get indices of selected items and sort in reverse to avoid index issues during deletion
            indices_to_delete = sorted([self.tree.index(item) for item in selected_items], reverse=True)

            for index in indices_to_delete:
                product_name = self.products[index].name
                del self.products[index]  # Remove product from the list
                self.status_bar.config(text=f"'{product_name}' product deleted.")  # Update status bar
            self.refresh_product_list()  # Update the Treeview display
            self.save_products()  # Save changes to file

    def update_stock(self):
        """
        Updates the stock quantity of the selected product.
        Allows updating only one product at a time.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a product to update its stock.")
            return

        if len(selected_items) > 1:
            messagebox.showwarning("Warning", "Please select only one product.")
            return

        index = self.tree.index(selected_items[0])  # Get the index of the selected item
        product = self.products[index]  # Get the Product object

        try:
            new_quantity = simpledialog.askinteger("Update Stock", f"Enter new stock quantity for '{product.name}':")
            if new_quantity is None:  # If user cancels
                return
            if new_quantity < 0:
                messagebox.showerror("Error", "Quantity cannot be negative.")
                return

            product.quantity = new_quantity  # Update the product's quantity
            self.refresh_product_list()  # Refresh the Treeview display
            self.status_bar.config(text=f"Stock quantity for '{product.name}' updated.")  # Update status bar
            self.save_products()  # Save changes to file
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a numeric value.")

    def refresh_product_list(self):
        """
        Clears the current Treeview display and repopulates it with the
        latest product data from the 'products' list.
        Applies color tags based on stock levels.
        """
        # Clear all existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert each product into the Treeview
        for i, product in enumerate(self.products):
            tags = ()
            # Apply 'red' tag if quantity is 5% or less of min_quantity
            if product.quantity <= product.min_quantity * 0.05:
                tags = ("red",)
            # Apply 'yellow' tag if quantity is 10% or less of min_quantity (but more than 5%)
            elif product.quantity <= product.min_quantity * 0.10:
                tags = ("yellow",)

            self.tree.insert("", tk.END, iid=i, values=(
                product.name,
                f"{product.price:.2f}",
                f"{product.price_with_vat:.2f}",
                product.quantity,
                product.min_quantity
            ), tags=tags)

        # Configure the visual appearance of the tags
        self.tree.tag_configure("red", background="red", foreground="white")
        self.tree.tag_configure("yellow", background="yellow", foreground="black")

    def show_selected_product_details(self, event):
        """
        Displays details of the selected product in the status bar when a row is clicked.

        Args:
            event (tk.Event): The event object generated by the click.
        """
        selected_items = self.tree.selection()
        if selected_items:
            index = self.tree.index(selected_items[0])  # Get the index of the first selected item
            product = self.products[index]  # Get the corresponding Product object
            self.status_bar.config(text=f"Selected Product: {product.name} | Stock: {product.quantity} | Min: {product.min_quantity}")
        else:
            self.status_bar.config(text="Ready")  # Reset status bar if no item is selected

    def save_products(self):
        """
        Saves the current list of products to the specified file in CSV format.
        """
        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                for product in self.products:
                    f.write(product.to_csv_row() + '\n')  # Write each product as a CSV row
            self.status_bar.config(text=f"Product data saved to '{self.file_name}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")
            self.status_bar.config(text="Data saving error!")

    def load_products(self):
        """
        Loads product data from the specified file into the application.
        Handles FileNotFoundError if the file does not exist.
        """
        self.products = []  # Clear current product list before loading
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    product = Product.from_csv_row(line)  # Create Product object from CSV row
                    if product:
                        self.products.append(product)  # Add valid product to the list
                    else:
                        self.status_bar.config(text=f"Skipped invalid row from file: {line.strip()}")
            self.refresh_product_list()  # Update the Treeview display with loaded data
            self.status_bar.config(text=f"Product data loaded from '{self.file_name}'.")
        except FileNotFoundError:
            self.status_bar.config(text="Stock file not found. A new file will be created.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading data: {e}")
            self.status_bar.config(text="Data loading error!")