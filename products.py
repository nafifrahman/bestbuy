"""Product management for the Best Buy store."""


class Product:
    """Represent a product and its available stock."""

    def __init__(self, name, price, quantity):
        """Initialize a product after validating its details."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Quantity must be a whole number.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name.strip()
        self.price = float(price)
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        """Return the available quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Update the quantity and deactivate if stock reaches zero."""
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Quantity must be a whole number.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self):
        """Return whether the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def show(self):
        """Print the product details."""
        print(
            f"{self.name}, Price: {self.price:g}, "
            f"Quantity: {self.quantity}"
        )

    def buy(self, quantity):
        """Purchase items, update stock, and return the total price."""
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Purchase quantity must be a whole number.")

        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")

        if not self.is_active():
            raise ValueError("This product is not active.")

        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)

        return total_price


def main():
    """Run the assignment's Product examples."""
    bose = Product(
        "Bose QuietComfort Earbuds",
        price=250,
        quantity=500,
    )

    mac = Product(
        "MacBook Air M2",
        price=1450,
        quantity=100,
    )

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()

    print("\n--- Testing insufficient stock ---")

    try:
        bose.buy(2000)
    except ValueError as error:
        print(error)

    print("Stock after failed purchase:", bose.get_quantity())

    print("\n--- Testing an invalid product ---")

    try:
        Product("", price=100, quantity=10)
    except ValueError as error:
        print(error)

    print("\n--- Testing a sold-out product ---")

    try:
        mac.buy(1)
    except ValueError as error:
        print(error)

    print("\n--- Testing restocking ---")

    mac.set_quantity(5)
    mac.activate()

    print("Active after restocking:", mac.is_active())
    print("Purchase total:", mac.buy(2))
    print("Remaining stock:", mac.get_quantity())

if __name__ == "__main__":
    main()
