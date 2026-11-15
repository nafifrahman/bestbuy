"""Store management for the Best Buy application."""

import products


class Store:
    """Manage a collection of products and customer orders."""

    def __init__(self, product_list):
        """Initialize the store with a list of products."""
        self.products = list(product_list)

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self):
        """Return the total number of items in stock."""
        total_quantity = 0

        for product in self.products:
            total_quantity += product.get_quantity()

        return total_quantity

    def get_all_products(self):
        """Return a list containing only active products."""
        active_products = []

        for product in self.products:
            if product.is_active():
                active_products.append(product)

        return active_products

    def order(self, shopping_list):
        """Validate an order, purchase its items, and return the total."""
        requested_quantities = {}

        # Validate the complete order before changing any stock.
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError("Product is not available in this store.")

            if isinstance(quantity, bool) or not isinstance(quantity, int):
                raise ValueError("Order quantity must be a whole number.")

            if quantity <= 0:
                raise ValueError("Order quantity must be greater than zero.")

            if not product.is_active():
                raise ValueError(f"{product.name} is not active.")

            requested_quantities[product] = (
                requested_quantities.get(product, 0) + quantity
            )

        for product, quantity in requested_quantities.items():
            if quantity > product.get_quantity():
                raise ValueError(
                    f"Not enough stock for {product.name}. "
                    f"Available: {product.get_quantity()}, "
                    f"requested: {quantity}."
                )

        total_price = 0.0

        for product, quantity in requested_quantities.items():
            total_price += product.buy(quantity)

        return total_price


def main():
    """Run the assignment's Store example."""
    product_list = [
        products.Product(
            "MacBook Air M2",
            price=1450,
            quantity=100,
        ),
        products.Product(
            "Bose QuietComfort Earbuds",
            price=250,
            quantity=500,
        ),
        products.Product(
            "Google Pixel 7",
            price=500,
            quantity=250,
        ),
    ]

    best_buy = Store(product_list)
    available_products = best_buy.get_all_products()

    print(best_buy.get_total_quantity())

    print(
        best_buy.order([
            (available_products[0], 1),
            (available_products[1], 2),
        ])
    )

    print("Stock after order:", best_buy.get_total_quantity())

    print("\n--- Repeated product test ---")

    bose = available_products[1]

    repeated_order_total = best_buy.order([
        (bose, 5),
        (bose, 10),
    ])

    print("Order cost:", repeated_order_total)
    print("Bose stock:", bose.get_quantity())

    print("\n--- Failed order test ---")

    mac = available_products[0]
    stock_before = best_buy.get_total_quantity()

    try:
        best_buy.order([
            (bose, 1),
            (mac, 1000),
        ])
    except ValueError as error:
        print(error)

    stock_after = best_buy.get_total_quantity()

    print("Stock unchanged:", stock_before == stock_after)


if __name__ == "__main__":
    main()