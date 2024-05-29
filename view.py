class View:
    def display_main_menu(self):
        print("1. View Products")
        print("2. Admin Login")
        print("3. Exit")

    def display_admin_login(self):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        return username, password

    def display_admin_menu(self):
        print("1. Add Product")
        print("2. Update Product")
        print("3. View Products")
        print("4. Logout")

    def display_add_product(self):
        product_name = input("Enter product name: ")
        price = input("Enter product price: ")  # Collecting as string initially
        emoji = input("Enter product emoji: ")
        return product_name, price, emoji

    def display_update_product(self):
        product_name = input("Enter product name: ")
        price = input("Enter new price: ")  # Collecting as string initially
        emoji = input("Enter new emoji: ")
        return product_name, price, emoji

    def display_products(self, products):
        for name, details in products.items():
            print(f"{name.capitalize()} ({details['emoji']}): ${details['price']} - {details['description']}")

    def display_order_details(self, order_details, total_price):
        print("Order details:")
        for product, quantity in order_details.items():
            print(f"{product}: {quantity}")
        print(f"Total price: ${total_price}")

    def confirm_order(self):
        confirmation = input("Confirm order? (yes/no): ")
        return confirmation.lower() == 'yes'

    def display_invalid_input(self, message):
        print(f"Invalid input: {message}")
