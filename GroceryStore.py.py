import tkinter as tk
from tkinter import messagebox
import pandas as pd
print("-----------------------Grocery Store Management System --------------------")
# Backend - GroceryStore class
class GroceryStore:
    def __init__(self):
        # Initial Inventory Setup with serial numbers
        self.inventory = {
            'Serial No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # Add Serial Numbers
            'Item': ['Dal', 'Chawal', 'Tel', 'Masala', 'Snacks','Kaju','Sugar', 'Rice', 'Wheat Flour', 'Ghee', 'Tea',
                     'Salt', 'Soap', 'Shampoo', 'Juice', 'Biscuits', 'Coffee'],
            'Unit Price (₹)': [40, 60, 80, 30, 20, 599, 42, 22, 23, 44, 344, 234, 45, 56, 78, 733, 5],  # Prices per kg
            'Stock (Kg)': [100, 50, 60, 120, 200, 20, 100, 8, 78, 9, 98, 23, 54, 3, 45, 11, 43]  # Quantities in kg
        }
        # Convert inventory to pandas DataFrame
        self.inventory_df = pd.DataFrame(self.inventory)

    def add_item(self, item_name, price, quantity_kg):
        """ Adds a new item to the store or updates existing stock in kg """
        if item_name in self.inventory_df['Item'].values:
            self.inventory_df.loc[self.inventory_df['Item'] == item_name, 'Stock (Kg)'] += quantity_kg
            return f"Updated stock for {item_name} by {quantity_kg} kg."
        else:
            new_serial_no = self.inventory_df['Serial No'].max() + 1  # Get the next serial number
            new_item = pd.DataFrame({
                'Serial No': [new_serial_no],
                'Item': [item_name],
                'Unit Price (₹)': [price],
                'Stock (Kg)': [quantity_kg]
            })
            self.inventory_df = pd.concat([self.inventory_df, new_item], ignore_index=True)
            return f"Added new item: {item_name} with {quantity_kg} kg stock."

    def update_price(self, item_name, new_price):
        """ Update the price of an existing item """
        if item_name in self.inventory_df['Item'].values:
            self.inventory_df.loc[self.inventory_df['Item'] == item_name, 'Unit Price (₹)'] = new_price
            return f"Updated price for {item_name} to {new_price}."
        else:
            return f"{item_name} does not exist in inventory."

    def change_quantity(self, item_name, quantity_change):
        """ Change the quantity of an item (increase or decrease) """
        if item_name in self.inventory_df['Item'].values:
            current_stock = self.inventory_df.loc[self.inventory_df['Item'] == item_name, 'Stock (Kg)'].iloc[0]
            new_stock = current_stock + quantity_change
            if new_stock < 0:
                return f"Not enough stock to decrease {item_name} by {abs(quantity_change)} kg."
            else:
                self.inventory_df.loc[self.inventory_df['Item'] == item_name, 'Stock (Kg)'] = new_stock
                return f"Updated stock for {item_name} by {quantity_change} kg."
        else:
            return f"{item_name} does not exist in inventory."

    def delete_item(self, item_name):
        """ Delete an item from the inventory """
        if item_name in self.inventory_df['Item'].values:
            self.inventory_df = self.inventory_df[self.inventory_df['Item'] != item_name]
            return f"Deleted {item_name} from the inventory."
        else:
            return f"{item_name} does not exist in inventory."

    def sell_item(self, item_name, quantity_kg):
        """ Sells an item and updates the stock in kg """
        if item_name not in self.inventory_df['Item'].values:
            return f"{item_name} not available in inventory."

        item_row = self.inventory_df[self.inventory_df['Item'] == item_name].iloc[0]
        stock_left = item_row['Stock (Kg)']
        price = item_row['Unit Price (₹)']

        if stock_left >= quantity_kg:
            total_cost = price * quantity_kg
            # Update stock after sale
            self.inventory_df.loc[self.inventory_df['Item'] == item_name, 'Stock (Kg)'] -= quantity_kg
            return f"Sold {quantity_kg} kg of {item_name}. Total cost: {total_cost}."
        else:
            return f"Not enough stock for {item_name}. Only {stock_left} kg left."

    def get_inventory(self):
        """ Returns the current inventory as a string """
        return self.inventory_df.to_string(index=False)


# Frontend - GUI Implementation using Tkinter
class GroceryStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Store Management System")

        self.store = GroceryStore()

        self.create_widgets()
        self.update_inventory_display()

    def create_widgets(self):
        # Add item frame
        add_item_frame = tk.LabelFrame(self.root, text="Add Item to Store", padx=10, pady=10)
        add_item_frame.grid(row=0, column=0, padx=20, pady=20)

        tk.Label(add_item_frame, text="Item Name:").grid(row=0, column=0)
        self.item_name_entry = tk.Entry(add_item_frame)
        self.item_name_entry.grid(row=0, column=1)

        tk.Label(add_item_frame, text="Price (per kg):").grid(row=1, column=0)
        self.price_entry = tk.Entry(add_item_frame)
        self.price_entry.grid(row=1, column=1)

        tk.Label(add_item_frame, text="Quantity (kg):").grid(row=2, column=0)
        self.quantity_entry = tk.Entry(add_item_frame)
        self.quantity_entry.grid(row=2, column=1)

        add_item_button = tk.Button(add_item_frame, text="Add Item", command=self.add_item)
        add_item_button.grid(row=3, column=0, columnspan=2)

        # Update price frame
        update_price_frame = tk.LabelFrame(self.root, text="Update Price", padx=10, pady=10)
        update_price_frame.grid(row=1, column=0, padx=20, pady=20)

        tk.Label(update_price_frame, text="Item Name:").grid(row=0, column=0)
        self.item_name_update_entry = tk.Entry(update_price_frame)
        self.item_name_update_entry.grid(row=0, column=1)

        tk.Label(update_price_frame, text="New Price (per kg):").grid(row=1, column=0)
        self.price_update_entry = tk.Entry(update_price_frame)
        self.price_update_entry.grid(row=1, column=1)

        update_price_button = tk.Button(update_price_frame, text="Update Price", command=self.update_price)
        update_price_button.grid(row=2, column=0, columnspan=2)

        # Change quantity frame
        change_quantity_frame = tk.LabelFrame(self.root, text="Update Quantity", padx=10, pady=10)
        change_quantity_frame.grid(row=2, column=0, padx=20, pady=20)

        tk.Label(change_quantity_frame, text="Item Name:").grid(row=0, column=0)
        self.item_name_change_entry = tk.Entry(change_quantity_frame)
        self.item_name_change_entry.grid(row=0, column=1)

        tk.Label(change_quantity_frame, text="Quantity Change (kg):").grid(row=1, column=0)
        self.quantity_change_entry = tk.Entry(change_quantity_frame)
        self.quantity_change_entry.grid(row=1, column=1)

        change_quantity_button = tk.Button(change_quantity_frame, text="Change Quantity", command=self.change_quantity)
        change_quantity_button.grid(row=2, column=0, columnspan=2)

        # Delete item frame
        delete_item_frame = tk.LabelFrame(self.root, text="Delete Item", padx=10, pady=10)
        delete_item_frame.grid(row=3, column=0, padx=20, pady=20)

        tk.Label(delete_item_frame, text="Item Name:").grid(row=0, column=0)
        self.item_name_delete_entry = tk.Entry(delete_item_frame)
        self.item_name_delete_entry.grid(row=0, column=1)

        delete_item_button = tk.Button(delete_item_frame, text="Delete Item", command=self.delete_item)
        delete_item_button.grid(row=1, column=0, columnspan=2)

        # Sell item frame
        sell_item_frame = tk.LabelFrame(self.root, text="Sell Item", padx=10, pady=10)
        sell_item_frame.grid(row=4, column=0, padx=20, pady=20)

        tk.Label(sell_item_frame, text="Item Name:").grid(row=0, column=0)
        self.item_name_sell_entry = tk.Entry(sell_item_frame)
        self.item_name_sell_entry.grid(row=0, column=1)

        tk.Label(sell_item_frame, text="Quantity (kg):").grid(row=1, column=0)
        self.quantity_sell_entry = tk.Entry(sell_item_frame)
        self.quantity_sell_entry.grid(row=1, column=1)

        sell_item_button = tk.Button(sell_item_frame, text="Sell Item", command=self.sell_item)
        sell_item_button.grid(row=2, column=0, columnspan=2)

        # Inventory display
        self.inventory_display = tk.Text(self.root, width=50, height=10)
        self.inventory_display.grid(row=0, column=1, rowspan=5, padx=20, pady=20)

    def update_inventory_display(self):
        """ Update the inventory display in the GUI """
        self.inventory_display.delete(1.0, tk.END)  # Clear previous display
        self.inventory_display.insert(tk.END, self.store.get_inventory())

    def add_item(self):
        """ Add a new item to the store using backend logic """
        item_name = self.item_name_entry.get()
        price = self.price_entry.get()
        quantity_kg = self.quantity_entry.get()

        if not item_name or not price.isdigit() or not quantity_kg.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        price = float(price)
        quantity_kg = float(quantity_kg)

        result = self.store.add_item(item_name, price, quantity_kg)
        messagebox.showinfo("Result", result)
        self.update_inventory_display()

    def update_price(self):
        """ Update the price of an item """
        item_name = self.item_name_update_entry.get()
        new_price = self.price_update_entry.get()

        if not item_name or not new_price.isdigit():
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        new_price = float(new_price)

        result = self.store.update_price(item_name, new_price)
        messagebox.showinfo("Result", result)
        self.update_inventory_display()

    def change_quantity(self):
        """ Change the quantity of an item """
        item_name = self.item_name_change_entry.get()
        quantity_change = self.quantity_change_entry.get()

        if not item_name or not quantity_change.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        quantity_change = float(quantity_change)

        result = self.store.change_quantity(item_name, quantity_change)
        messagebox.showinfo("Result", result)
        self.update_inventory_display()

    def delete_item(self):
        """ Delete an item from the inventory """
        item_name = self.item_name_delete_entry.get()

        if not item_name:
            messagebox.showerror("Input Error", "Please enter an item name to delete.")
            return

        result = self.store.delete_item(item_name)
        messagebox.showinfo("Result", result)
        self.update_inventory_display()

    def sell_item(self):
        """ Sell an item to a customer using backend logic """
        item_name = self.item_name_sell_entry.get()
        quantity_kg = self.quantity_sell_entry.get()

        if not item_name or not quantity_kg.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        quantity_kg = float(quantity_kg)

        result = self.store.sell_item(item_name, quantity_kg)
        messagebox.showinfo("Result", result)
        self.update_inventory_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryStoreApp(root)
    root.mainloop()
