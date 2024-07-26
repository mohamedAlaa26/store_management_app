from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
from models import Item, Sale, Ticket, User, session
import generate_ticket
from login import login_user
from werkzeug.security import generate_password_hash

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Management")
        self.root.geometry("900x600")
        set_appearance_mode("dark")
        set_default_color_theme("green")

        self.current_user = None

        self.setup_ui()

    def setup_ui(self):
        # Login Frame
        self.login_frame = CTkFrame(master=self.root)
        self.login_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.username_label = CTkLabel(self.login_frame, text="Username")
        self.username_label.pack(pady=(20, 10))
        self.username_entry = CTkEntry(self.login_frame, placeholder_text="Enter your username")
        self.username_entry.pack(pady=10)

        self.password_label = CTkLabel(self.login_frame, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = CTkEntry(self.login_frame, placeholder_text="Enter your password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=(20, 10))

        # Admin Frame
        self.admin_frame = CTkFrame(master=self.root)
        self.admin_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.admin_frame.pack_forget()

        self.add_user_button = CTkButton(self.admin_frame, text="Add User", command=self.show_add_user)
        self.add_user_button.pack(pady=10)

        self.view_sales_button = CTkButton(self.admin_frame, text="View Sales", command=self.view_sales)
        self.view_sales_button.pack(pady=10)

        self.view_items_button = CTkButton(self.admin_frame, text="View Items", command=self.view_items)
        self.view_items_button.pack(pady=10)

        self.total_cost_button = CTkButton(self.admin_frame, text="Total Cost", command=self.total_cost)
        self.total_cost_button.pack(pady=10)

        # Add User Frame
        self.add_user_frame = CTkFrame(master=self.root)
        self.add_user_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.add_user_frame.pack_forget()

        self.new_username_label = CTkLabel(self.add_user_frame, text="New Username")
        self.new_username_label.pack(pady=(20, 10))
        self.new_username_entry = CTkEntry(self.add_user_frame, placeholder_text="Enter new username")
        self.new_username_entry.pack(pady=10)

        self.new_password_label = CTkLabel(self.add_user_frame, text="New Password")
        self.new_password_label.pack(pady=10)
        self.new_password_entry = CTkEntry(self.add_user_frame, placeholder_text="Enter new password", show="*")
        self.new_password_entry.pack(pady=10)

        self.create_user_button = CTkButton(self.add_user_frame, text="Create User", command=self.create_user)
        self.create_user_button.pack(pady=(20, 10))

        # User Menu Frame
        self.user_menu_frame = CTkFrame(master=self.root)
        self.user_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.user_menu_frame.pack_forget()

        self.add_item_button = CTkButton(self.user_menu_frame, text="Add Item", command=self.show_add_item)
        self.add_item_button.pack(pady=10)

        self.sell_item_button = CTkButton(self.user_menu_frame, text="Sell Item", command=self.show_sell_item)
        self.sell_item_button.pack(pady=10)

        self.view_added_items_button = CTkButton(self.user_menu_frame, text="View Added Items", command=self.show_view_added_items)
        self.view_added_items_button.pack(pady=10)

        self.view_sold_items_button = CTkButton(self.user_menu_frame, text="View Sold Items", command=self.show_view_sold_items)
        self.view_sold_items_button.pack(pady=10)

        # Add Item Frame
        self.add_item_frame = CTkFrame(master=self.root)
        self.add_item_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.add_item_frame.pack_forget()

        self.name_label = CTkLabel(self.add_item_frame, text="Item Name")
        self.name_label.pack(pady=(20, 10))
        self.name_entry = CTkEntry(self.add_item_frame, placeholder_text="Enter item name")
        self.name_entry.pack(pady=10)

        self.quantity_label = CTkLabel(self.add_item_frame, text="Quantity")
        self.quantity_label.pack(pady=10)
        self.quantity_entry = CTkEntry(self.add_item_frame, placeholder_text="Enter quantity")
        self.quantity_entry.pack(pady=10)

        self.price_label = CTkLabel(self.add_item_frame, text="Price")
        self.price_label.pack(pady=10)
        self.price_entry = CTkEntry(self.add_item_frame, placeholder_text="Enter price")
        self.price_entry.pack(pady=10)

        self.category_label = CTkLabel(self.add_item_frame, text="Category")
        self.category_label.pack(pady=10)
        self.category_entry = CTkEntry(self.add_item_frame, placeholder_text="Enter category")
        self.category_entry.pack(pady=10)

        self.add_button = CTkButton(self.add_item_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(pady=(20, 10))

        self.back_to_menu_button1 = CTkButton(self.add_item_frame, text="Back to Menu", command=self.show_user_menu)
        self.back_to_menu_button1.pack(pady=10)

        # Sell Item Frame
        self.sell_item_frame = CTkFrame(master=self.root)
        self.sell_item_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.sell_item_frame.pack_forget()

        self.sell_label = CTkLabel(self.sell_item_frame, text="Sell Item ID")
        self.sell_label.pack(pady=(20, 10))
        self.sell_entry = CTkEntry(self.sell_item_frame, placeholder_text="Enter item ID to sell")
        self.sell_entry.pack(pady=10)

        self.sell_quantity_label = CTkLabel(self.sell_item_frame, text="Quantity to Sell")
        self.sell_quantity_label.pack(pady=10)
        self.sell_quantity_entry = CTkEntry(self.sell_item_frame, placeholder_text="Enter quantity to sell")
        self.sell_quantity_entry.pack(pady=10)

        self.sell_button = CTkButton(self.sell_item_frame, text="Sell Item", command=self.sell_item)
        self.sell_button.pack(pady=(20, 10))

        self.back_to_menu_button2 = CTkButton(self.sell_item_frame, text="Back to Menu", command=self.show_user_menu)
        self.back_to_menu_button2.pack(pady=10)

        # View Added Items Frame
        self.view_added_items_frame = CTkFrame(master=self.root)
        self.view_added_items_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.view_added_items_frame.pack_forget()

        self.added_items_tree = ttk.Treeview(self.view_added_items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Date Added'), show='headings')
        self.added_items_tree.heading('ID', text='ID')
        self.added_items_tree.heading('Name', text='Name')
        self.added_items_tree.heading('Quantity', text='Quantity')
        self.added_items_tree.heading('Price', text='Price')
        self.added_items_tree.heading('Date Added', text='Date Added')
        self.added_items_tree.pack(pady=10)

        self.back_to_menu_button3 = CTkButton(self.view_added_items_frame, text="Back to Menu", command=self.show_user_menu)
        self.back_to_menu_button3.pack(pady=10)

        # View Sold Items Frame
        self.view_sold_items_frame = CTkFrame(master=self.root)
        self.view_sold_items_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.view_sold_items_frame.pack_forget()

        self.sold_items_tree = ttk.Treeview(self.view_sold_items_frame, columns=('Sale ID', 'Item Name', 'Quantity', 'Total Price', 'Date Sold'), show='headings')
        self.sold_items_tree.heading('Sale ID', text='Sale ID')
        self.sold_items_tree.heading('Item Name', text='Item Name')
        self.sold_items_tree.heading('Quantity', text='Quantity')
        self.sold_items_tree.heading('Total Price', text='Total Price')
        self.sold_items_tree.heading('Date Sold', text='Date Sold')
        self.sold_items_tree.pack(pady=10)

        self.back_to_menu_button4 = CTkButton(self.view_sold_items_frame, text="Back to Menu", command=self.show_user_menu)
        self.back_to_menu_button4.pack(pady=10)

    def show_user_menu(self):
        self.hide_all_frames()
        self.user_menu_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def show_add_user(self):
        self.hide_all_frames()
        self.add_user_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def show_add_item(self):
        self.hide_all_frames()
        self.add_item_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def show_sell_item(self):
        self.hide_all_frames()
        self.sell_item_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def show_view_added_items(self):
        self.hide_all_frames()
        self.view_added_items_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.load_added_items()

    def show_view_sold_items(self):
        self.hide_all_frames()
        self.view_sold_items_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.load_sold_items()

    def hide_all_frames(self):
        self.login_frame.pack_forget()
        self.admin_frame.pack_forget()
        self.add_user_frame.pack_forget()
        self.user_menu_frame.pack_forget()
        self.add_item_frame.pack_forget()
        self.sell_item_frame.pack_forget()
        self.view_added_items_frame.pack_forget()
        self.view_sold_items_frame.pack_forget()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = login_user(username, password)
        if user:
            self.current_user = user
            self.hide_all_frames()
            if user.username == 'root':
                self.admin_frame.pack(padx=20, pady=20, fill="both", expand=True)
            else:
                self.show_user_menu()
            messagebox.showinfo("Info", f"User {username} logged in successfully!")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        hashed_password = generate_password_hash(new_password)
        new_user = User(username=new_username, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        messagebox.showinfo("Info", "User created successfully.")
        self.show_user_menu()

    def view_sales(self):
        sales = session.query(Sale).all()
        sales_info = ""
        for sale in sales:
            item = session.query(Item).filter_by(id=sale.item_id).first()
            user = session.query(User).filter_by(id=sale.sold_by).first()
            sales_info += f"Sale ID: {sale.id}, Item: {item.name}, Quantity: {sale.quantity_sold}, Total: {sale.total_price}, Sold by: {user.username}\n"
        messagebox.showinfo("Sales Info", sales_info)

    def view_items(self):
        items = session.query(Item).all()
        items_info = ""
        for item in items:
            items_info += f"Item ID: {item.id}, Name: {item.name}, Quantity: {item.quantity}, Price: {item.price}, Category: {item.category}\n"
        messagebox.showinfo("Items Info", items_info)

    def total_cost(self):
        items = session.query(Item).all()
        total_cost = sum(item.quantity * item.price for item in items)
        messagebox.showinfo("Total Cost", f"The total cost of all items in the store is: {total_cost}")

    def add_item(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to add items.")
            return
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        category = self.category_entry.get()
        item = Item(name=name, description="", quantity=quantity, price=price, category=category, added_by=self.current_user.id)
        session.add(item)
        session.commit()
        messagebox.showinfo("Info", "Item added successfully!")

    def sell_item(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to sell items.")
            return
        item_id = int(self.sell_entry.get())
        quantity_sold = int(self.sell_quantity_entry.get())
        item = session.query(Item).filter_by(id=item_id).first()

        if item and item.quantity >= quantity_sold:
            total_price = item.price * quantity_sold
            sale = Sale(item_id=item_id, quantity_sold=quantity_sold, total_price=total_price, sold_by=self.current_user.id)
            session.add(sale)
            item.quantity -= quantity_sold
            session.commit()

            generate_ticket.generate_ticket(sale.id)
            messagebox.showinfo("Info", "Item sold and ticket generated!")
        else:
            messagebox.showerror("Error", "Item not found or insufficient quantity")

    def view_added_items(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to view items.")
            return
        items = session.query(Item).filter_by(added_by=self.current_user.id).all()
        items_info = ""
        for item in items:
            items_info += f"Item ID: {item.id}, Name: {item.name}, Quantity: {item.quantity}, Price: {item.price}, Date Added: {item.added_by}\n"
        messagebox.showinfo("Added Items", items_info)

    def view_sold_items(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to view items.")
            return
        sales = session.query(Sale).filter_by(sold_by=self.current_user.id).all()
        sales_info = ""
        for sale in sales:
            item = session.query(Item).filter_by(id=sale.item_id).first()
            sales_info += f"Sale ID: {sale.id}, Item: {item.name}, Quantity: {sale.quantity_sold}, Total: {sale.total_price}, Date Sold: {sale.sale_date}\n"
        messagebox.showinfo("Sold Items", sales_info)

if __name__ == "__main__":
    root = CTk()
    app = StoreApp(root)
    root.mainloop()
