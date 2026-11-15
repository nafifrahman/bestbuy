"""Command-line interface for the Best Buy store."""

import products
import store


def list_products(best_buy):
    """Display active products and return the displayed list."""
    available_products = best_buy.get_all_products()

    if not available_products:
        print("No active products are available.")
        return available_products

    print("\nAvailable products:")
    print("-------------------")

    for number, product in enumerate(available_products, start=1):
        print(f"{number}. ", end="")
        product.show()

    return available_products


def make_order(best_buy):
    """Collect a shopping list and submit it to the store."""
    available_products = list_products(best_buy)

    if not available_products:
        return

    shopping_list = []
    pending_quantities = {}

    print("\nChoose products using their displayed numbers.")
    print("Press Enter at the product prompt to finish your order.")

    while True:
        product_choice = input("\nProduct number: ").strip()

        if product_choice == "":
            break

        try:
            product_number = int(product_choice)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if product_number < 1 or product_number > len(available_products):
            print("Please choose a product number from the list.")
            continue

        product = available_products[product_number - 1]

        quantity_choice = input("Quantity: ").strip()

        try:
            quantity = int(quantity_choice)
        except ValueError:
            print("Please enter a whole number for the quantity.")
            continue

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue

        already_selected = pending_quantities.get(product, 0)
        remaining_quantity = product.get_quantity() - already_selected

        if quantity > remaining_quantity:
            print(
                f"Not enough stock. You can add up to "
                f"{remaining_quantity} more."
            )
            continue

        shopping_list.append((product, quantity))
        pending_quantities[product] = already_selected + quantity

        print(f"Added {quantity} x {product.name} to your order.")

    if not shopping_list:
        print("No items selected. Returning to the main menu.")
        return

    try:
        total_price = best_buy.order(shopping_list)
    except ValueError as error:
        print(f"Order failed: {error}")
    else:
        print(f"\nOrder completed! Total price: ${total_price:.2f}")


def start(best_buy):
    """Display the store menu until the user quits."""
    while True:
        print("\nBest Buy")
        print("--------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            list_products(best_buy)

        elif choice == "2":
            total_quantity = best_buy.get_total_quantity()
            print(f"Total items in store: {total_quantity}")

        elif choice == "3":
            make_order(best_buy)

        elif choice == "4":
            print("Thank you for visiting Best Buy. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


def main():
    """Create the initial inventory and start the application."""
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

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
