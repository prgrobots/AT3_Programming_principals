# controller
from model import Model
from view import View

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view    

    def run(self):
        while True:
            self.view.display_main_menu()
            choice = input("Select an option: ")
            if choice == '1':
                self.show_products()
            elif choice == '2':
                self.admin_login()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def show_products(self):
        products = self.model.get_products()
        self.view.display_products(products)

    def admin_login(self):
        username, password = self.view.display_admin_login()        
        if username == "" and password == "":  
            self.admin_menu()
        else:
            print("Invalid credentials. Please try again.")

    def admin_menu(self):        
            self.view.display_admin_menu()
            choice = input("Select an option: ")
            if choice == '1':
                self.add_product()  
            elif choice == '2':
                self.show_products()
            else:
                print("Invalid choice. Please try again.")

    def add_product(self):
        product_name, price, emoji = self.view.display_add_product()
        if not product_name or not emoji:
            self.view.display_invalid_input("Fields cannot be empty.")
            # return False
        try:
            float(price)
        except ValueError:
            self.view.display_invalid_input("Price must be a number")
            return
        self.model.add_or_update_product(product_name, price, emoji)
        print("Product added successfully.")

    # def update_product(self):
    #     product_name, price, emoji = self.view.display_update_product()
        
    #     self.model.add_or_update_product(product_name, price, emoji)
    #     print("Product updated successfully.")

    def validate_product_input(self, product_name, price, emoji):
              
        if not product_name or not emoji:
            self.view.display_invalid_input("Cannot be empty.")
            # return False
        try:
            float(price)
        except ValueError as e:
            self.view.display_invalid_input(e) 
        # return True


if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run()
