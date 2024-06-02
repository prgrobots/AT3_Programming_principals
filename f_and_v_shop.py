import os
import tkinter as tk
from tkinter import PhotoImage, messagebox
from PIL import ImageTk, Image
from database import fruit_veg_database

class FruitVegApp:
    '''
    Initializes the root window and sets up the dictionary to store entry widgets for each product.
    '''
    def __init__(self, root):
        self.root = root
        self.entries = {}  # Dictionary to store entry widgets for each product
        self.show_main_menu()  # Show the main menu when the app starts


    def clear_window(self):
        '''Clears the window by destroying all widgets.'''
        for widget in self.root.winfo_children():
            widget.destroy()


    def show_login(self):
        '''
        Displays the login screen with username and password entry fields.
        '''
        self.clear_window()  # Clear the window before showing the login screen
        login_frame = tk.Frame(self.root)
        login_frame.pack()
        tk.Label(login_frame, text='Login').pack() 
        tk.Label(login_frame, text='Username').pack() 
        username_entry = tk.Entry(login_frame)
        username_entry.pack()
        tk.Label(login_frame, text='Password').pack()
        password_entry = tk.Entry(login_frame, show='*')  # Hide the password with asterisks
        password_entry.pack()
        tk.Button(login_frame, text='Login', command=lambda: self.validate_login(username_entry.get(), password_entry.get())).pack()
        tk.Button(login_frame, text='Main Menu', command=self.show_main_menu).pack()


    def validate_login(self, username, password):
        '''Dummy function to validate the entered login credentials.'''
        if username == 'admin' and password == '1234':
            messagebox.showinfo('Login Successful', 'Welcome, admin!')
            self.show_admin_menu()  # Show the admin menu for successful admin login
        elif username == 'customer' and password == '1234':
            messagebox.showinfo('Login Successful', 'Welcome, customer!')
            self.clear_window()  # Clear the window before showing products
            self.show_products()  # Show the products for successful customer login
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password')


    def show_main_menu(self):
        '''
        Displays the main menu with options to buy products or log in as an admin.
        '''
        self.clear_window()  # Clear the window before showing the main menu
        img = ImageTk.PhotoImage(Image.open('images/welcome.png'))  # Load the welcome image
        panel = tk.Label(self.root, image=img)
        panel.image = img  # Keep a reference to avoid garbage collection
        panel.pack(expand=True)  # Center the image in the middle
        # Creates the buttons and their function calls
        cust_button = tk.Button(self.root, text='Buy Products', font=('Arial', 18), command=self.show_login)
        admin_button = tk.Button(self.root, text='Admin Login', font=('Arial', 18), command=self.show_login)
        cust_button.place(x=320, y=380)  # Position the 'Buy Products' button
        admin_button.place(x=100, y=380)  # Position the 'Admin Login' button


    def button_creator(self, frame, image_path, name, price, row):
        '''
        Creates a button with an image, description, and amount entry for a product.
        '''
        image_path = os.path.join('images', image_path)  # Construct the image file path
        image = PhotoImage(file=image_path)  # Load the product image
        image_label = tk.Label(frame, image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection
        image_label.grid(row=row, column=0, padx=5)  # Position the image label in the grid

        desc_label = tk.Label(frame, text=name, font=('Arial', 20))  # Create a label for the product description
        desc_label.grid(row=row, column=1, padx=5)  # Position the description label in the grid

        entry = tk.Entry(frame, width=10)  # Create an entry widget for the amount
        entry.grid(row=row, column=2, padx=5)  # Position the entry widget in the grid
        self.entries[name] = (entry, price)  # Store the entry widget and price in the entries dictionary

        frame.pack(pady=10)  # Add spacing between product buttons


    def show_products(self):
        '''
        Displays the available products after a successful login.
        '''
        product_frame = tk.Frame(self.root)
        product_frame.pack()
        row = 0  # Counter for the row number
        for name, (image_path, price) in fruit_veg_database.items():
            self.button_creator(product_frame, image_path, name, price, row)  # Create a button for each product
            row += 1  # Increment the row number for the next product

        confirm_button = tk.Button(product_frame, text='Confirm Purchase', command=self.confirm_purchase)
        confirm_button.grid(row=row, column=3, pady=20)  # Position the 'Confirm Purchase' button
        menu_button = tk.Button(product_frame, text='Main menu', command=self.show_main_menu) # Go back to the menu
        menu_button.grid(row=row, column=0, pady=20)  # Position the 'Main menu' button
        quit_button = tk.Button(product_frame, text='Quit', command=self.root.quit) # Exit the program
        quit_button.grid(row=row, column=2, pady=60)  # Position the 'Quit' button


    def confirm_purchase(self):
        '''
        Shows the confirmation window and appends the order details to a file.
        '''
        total_cost = 0
        order_details = ''
        for name, (entry, price) in self.entries.items():
            try:
                amount = int(entry.get())  # Get the amount entered for each product
                if amount > 0:
                    item_total = amount * price  # Calculate the total cost for the item
                    total_cost += item_total  # Add the item total to the overall total cost
                    order_details += f'{name}: {amount} x ${price} = ${item_total}\n'  # Add the item details to the order summary
            except ValueError:
                pass  # Ignore invalid entries
        if total_cost > 0:
            order_details += f'\nTotal Purchase Amount: ${total_cost}'  # Add the total purchase amount to the order summary
            messagebox.showinfo('Order Confirmation', order_details)  # Show the order confirmation message
            
            os.makedirs('orders', exist_ok=True)  # Create the 'orders' directory if it doesn't exist
            file_path = os.path.join('orders', 'order_details.txt')  # Construct the file path for storing order details
            
            with open(file_path, 'a') as file:  # Open the file in append mode
                file.write(order_details + '\n\n')  # Append the order details to the file on a new line
        else:
            messagebox.showwarning('No Items', 'No items were selected for purchase.')


    def show_admin_menu(self):
        '''
        Displays the admin menu with options to add or update products.
        '''
        self.clear_window()  # Clear the window before showing the admin menu
        admin_frame = tk.Frame(self.root)
        admin_frame.pack()
        # Creating buttons and the label
        tk.Label(admin_frame, text='Admin Menu', font=('Arial', 24)).pack(pady=10)
        tk.Button(admin_frame, text='Add Product', command=self.add_product).pack(pady=5)
        tk.Button(admin_frame, text='Update Product', command=self.update_product).pack(pady=5)
        tk.Button(admin_frame, text='Main Menu', command=self.show_main_menu).pack(pady=5)
        tk.Button(admin_frame, text='Quit', command=self.root.quit).pack(pady=5)


    def add_product(self):
        '''
        Allows adding a new product with a name and price.
        '''
        self.clear_window()  # Clear the window before showing the add product form
        add_frame = tk.Frame(self.root)
        add_frame.pack()
        tk.Label(add_frame, text='Add New Product', font=('Arial', 24)).pack(pady=10)
        tk.Label(add_frame, text='Product Name').pack()
        name_entry = tk.Entry(add_frame)  # Entry field for the product name
        name_entry.pack()        
        tk.Label(add_frame, text='Price').pack()
        price_entry = tk.Entry(add_frame)  # Entry field for the product price
        price_entry.pack()
        # Creates a button that calls the save method
        tk.Button(add_frame, text='Add', command=lambda: self.save_product(name_entry.get(), price_entry.get())).pack(pady=10)
        tk.Button(add_frame, text='Admin Menu', command=self.show_admin_menu).pack(pady=5)
        


    def save_product(self, name, price):
        '''
        Saves the newly added product to the database.
        '''
        try:
            price = int(price)  # Convert the price to a int
            if name and price:
                fruit_veg_database[name] = (price)  # Add the new product to the database
                messagebox.showinfo('Product Added', f'{name} has been added to the database.')
                print(fruit_veg_database) # print the database to show the changes
                self.show_admin_menu()  # Return to the admin menu after adding the product
            else:
                messagebox.showerror('Error', 'All fields must be filled out.')
        except ValueError:
            messagebox.showerror('Error', 'Price must be a number.')


    def update_product(self):
        '''
        Allows updating the price of an existing product.
        '''
        self.clear_window()  # Clear the window before showing the update product form
        update_frame = tk.Frame(self.root)
        update_frame.pack()
        
        products = list(fruit_veg_database.keys())  # Get the list of product names from the database

        tk.Label(update_frame, text='Select Product to Update', font=('Arial', 24)).pack(pady=10)

        selected_product = tk.StringVar(update_frame)  # Variable to store the selected product
        selected_product.set(products[0])  # Set the default value to the first product
        
        product_dropdown = tk.OptionMenu(update_frame, selected_product, *products)  # Create a dropdown menu for selecting the product
        product_dropdown.pack(pady=5)
        tk.Label(update_frame, text='New Price').pack()
        price_entry = tk.Entry(update_frame)  # Entry field for the new price
        price_entry.pack()
        tk.Button(update_frame, text='Update', command=lambda: self.save_updated_product(selected_product.get(), price_entry.get())).pack(pady=10)
        tk.Button(update_frame, text='Admin Menu', command=self.show_admin_menu).pack(pady=5)


    def save_updated_product(self, name, new_price):
        '''
        Saves the updated product price to the database.
        '''
        try:
            new_price = float(new_price)  # Convert the new price to a float
            if name in fruit_veg_database:
                fruit_veg_database[name] = (fruit_veg_database[name][0], new_price)  # Update the price of the selected product
                messagebox.showinfo('Product Updated', f'{name} has been updated.')
                print(fruit_veg_database)  # Print the updated database 
                self.show_admin_menu()  # Return to the admin menu after updating the product
            else:
                messagebox.showerror('Error', 'Product not found.')
        except ValueError:
            messagebox.showerror('Error', 'Price must be a number.')

# Initialize the main window
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Fruit and Vegetable Database')
    app = FruitVegApp(root)
    root.mainloop()  # Start the main event loop