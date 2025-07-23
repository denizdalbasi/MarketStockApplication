class Product:
    """
    Represents a product with its details such as name, price, quantity,
    minimum quantity, and VAT rate.
    """
    def __init__(self, name, price, quantity, min_quantity):
        """
        Initializes a new Product object.

        Args:
            name (str): The name of the product.
            price (float or str): The base price of the product.
            quantity (int or str): The current stock quantity of the product.
            min_quantity (int or str): The minimum desired quantity for the product.
        """
        self.name = name
        self.price = float(price)  # Convert price to float
        self.quantity = int(quantity)  # Convert quantity to integer
        self.min_quantity = int(min_quantity)  # Convert minimum quantity to integer
        self.vat_rate = 0.18  # Assuming an 18% VAT rate

    @property
    def price_with_vat(self):
        """
        Calculates and returns the price of the product including VAT.

        Returns:
            float: The price of the product with VAT applied.
        """
        return self.price * (1 + self.vat_rate)

    def __str__(self):
        """
        Returns a string representation of the Product object.

        Returns:
            str: A formatted string displaying product details.
        """
        return (f"Product Name: {self.name}, Price: {self.price:.2f} TL, "
                f"Price with VAT: {self.price_with_vat:.2f} TL, Quantity: {self.quantity}, "
                f"Min Quantity: {self.min_quantity}")

    def to_csv_row(self):
        """
        Converts the Product object into a CSV formatted string row.

        Returns:
            str: A comma-separated string representing the product's data.
        """
        return f"{self.name},{self.price},{self.quantity},{self.min_quantity}"

    @staticmethod
    def from_csv_row(csv_row):
        """
        Creates a Product object from a CSV formatted string row.

        Args:
            csv_row (str): A comma-separated string representing product data.

        Returns:
            Product or None: A Product object if the row is valid, otherwise None.
        """
        parts = csv_row.strip().split(',')
        if len(parts) == 4:
            try:
                name = parts[0]
                price = float(parts[1])
                quantity = int(parts[2])
                min_quantity = int(parts[3])
                return Product(name, price, quantity, min_quantity)
            except ValueError:
                # Return None if there's a type conversion error (e.g., non-numeric price/quantity)
                return None
        # Return None if the row does not have the expected number of parts
        return None