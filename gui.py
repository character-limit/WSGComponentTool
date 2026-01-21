import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from user import User
from userdb import UserDB
from item import Item
from itemdb import ItemDB


""" window = tk.Tk()
window.title("WSG Component Tool")
window.geometry("900x600")

tk.Label(window, text="Username:").pack()
username_entry = tk.Entry(window)
username_entry.pack()


tk.Label(window, text="Password:").pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

tk.Button(window, text="Login", command=login).pack(pady=15)


window.mainloop() """

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        self.geometry("900x600")
        self.minsize(900,600)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (LoginPage, DashboardPage, InventoryPage, StockPage, AdminPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller

        label = tk.Label(self, text="Login Page")
        label.pack(pady=10, padx=10)

        tk.Label (self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        button1 = tk.Button(self, text="Login", command=self.login)
        button1.pack(pady=10)

    def login(self):
        #check entered fields
        username = self.username_entry.get().lower()
        password = self.password_entry.get()
        
        #if correct, update user session and naviagte to dashboard. Else show error
        if UserDB().check_login(username, password):
            self.controller.show_frame("DashboardPage")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
        

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller
        controller.title("Dashboard")

        #HEADER - inc back, title, and logout buttons
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="Dashboard")
        self.title_label.grid(row=0, column=1)#centre

        btn_logout = tk.Button(head_frame, text="Logout", command=self.logout)
        btn_logout.grid(row=0, column=2, sticky="e")#right

        #MENU BUTTONS - inventory, stock monitor, admin settings
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_inventory = tk.Button(center_frame, text="Manage\nInventory", width=30, height=13, command=self.open_inventory)
        btn_inventory.grid(row=0, column=0, padx=10)

        btn_stock = tk.Button(center_frame, text="Stock\nMonitor", width=30, height=13, command=self.open_stock_monitor)
        btn_stock.grid(row=0, column=1, padx=10)

        self.btn_admin = tk.Button(center_frame, text="Admin\nSettings", width=30, height=13, command=self.open_admin_settings)
        self.btn_admin.grid(row=0, column=2, padx=10)

    def logout(self):
        self.controller.show_frame("LoginPage")

    def back(self):
        pass

    def open_inventory(self):
        self.controller.show_frame("InventoryPage")

    def open_stock_monitor(self):
        self.controller.show_frame("StockPage")
    
    def open_admin_settings(self):
        if User.session.isAdmin:
            self.controller.show_frame("AdminPage")
        else:
            messagebox.showerror("Action Failed", "This menu requires elevated permissions, please contact the system manager for more information.")

    #update elements when frame is raised
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)

        self.title_label.config(text=f"Dashboard - {User.session.username}") #update username when raising frame

        """ if User.session.isAdmin == True:
            self.btn_admin.config(state="normal")
        else:
            self.btn_admin.config(state="disabled") """

class InventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller
        controller.title("Inventory Management")


        #HEADER - inc back, title, and logout buttons
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="Inventory Management")
        self.title_label.grid(row=0, column=1)#centre

        #SEARCH BAR 
        search_frame = tk.Frame(self)
        search_frame.pack(side="top", fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search Inventory:").pack(side="left", padx=5, pady=5)
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left", padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search) #dynamic search when each char entered.

        #TABLE
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Columns = ["Name", "Quantity", "Location", "Item ID"]
        self.tree = ttk.Treeview(table_frame, columns=Columns, show="headings")

        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Item ID", text="Item ID")

        self.tree.column("Name", width=250, anchor="center")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Location", width=150, anchor="center")
        self.tree.column("Item ID", width=100, anchor="center")

        scollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scollbar.pack(side="right", fill="y")

        #bottom buttons (delete item, add)
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side="bottom", fill="x", padx=10, pady=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        btn_delete = tk.Button(buttons_frame, text="Delete Selected Item", command=self.deleteItem)
        btn_delete.grid(row=0, column=0, sticky="w", padx=5)#left

        btn_edit = tk.Button(buttons_frame, text="Edit Selected Item", command=self.editItem)
        btn_edit.grid(row=0, column=1, sticky="w", padx=5)#left

        btn_add = tk.Button(buttons_frame, text="Add New Item", command=self.addItem)
        btn_add.grid(row=0, column=2, sticky="w", padx=5)#left

    def back(self):
        self.controller.show_frame("DashboardPage")

    def search(self, event):
        query = self.search_entry.get()
        for row in self.tree.get_children():
            self.tree.delete(row)

        items = ItemDB().get_items(query)

        if items:
            for item in items:
                self.tree.insert("", tk.END, values=(
                    item.name, 
                    item.quantity, 
                    item.location, 
                    item.ID
                ))

    def deleteItem(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item)["values"][3]#get id
            item_name = self.tree.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?")
            if confirm:
                ItemDB().remove_item(item_id)
                self.refresh_table()
        else:
            messagebox.showwarning("No Selection", "Please select an item to delete.")

    def editItem(self):

        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item)["values"][3]#get id
            selected = ItemDB().get_item(item_id)#get item

            #pu
            add_popup = tk.Toplevel(self)
            add_popup.title("Edit Item")
            add_popup.geometry("300x400")
            add_popup.grab_set()

            tk.Label(add_popup, text="Item Name:").pack(pady=5)
            name_entry = tk.Entry(add_popup)
            name_entry.pack()

            tk.Label(add_popup, text="Item Location:").pack(pady=5)
            location_entry = tk.Entry(add_popup)
            location_entry.pack()

            tk.Label(add_popup, text="Item Quantity:").pack(pady=5)
            quantity_entry = tk.Entry(add_popup)    
            quantity_entry.pack()

            #prefill data
            name_entry.insert(0, selected.name)
            location_entry.insert(0, selected.location)
            quantity_entry.insert(0, selected.quantity)
        else:
            messagebox.showwarning("No Selection", "Please select an item to edit.")

        def submit():
            name = name_entry.get()
            location = location_entry.get()
            quantity = quantity_entry.get()
            
            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity must be a number between 0 and 9999.")
                return
            
            if not name or not location or quantity < 0 or quantity > 9999:
                messagebox.showerror("Invalid Input", "Please provide valid item details.")
                return

            selected.name = name
            selected.location = location
            selected.quantity = int(quantity)
            ItemDB().edit_item(selected)
            messagebox.showinfo("Success", f"Item '{selected.name}' edited successfully.")
            add_popup.destroy()
            self.refresh_table()

        tk.Button(add_popup, text="Submit", command=submit, bg="green", fg="white").pack(pady=20)
    def refresh_table(self):
        self.search_entry.delete(0, tk.END)#clear search bar

        for row in self.tree.get_children():
            self.tree.delete(row)#clear all rows
        
        items = ItemDB().get_items("")  #get all items

        if items:
            for item in items:
                self.tree.insert("", tk.END, values=(item.name, item.quantity, item.location, item.ID))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_table()

    def addItem(self):
        #pu
        add_popup = tk.Toplevel(self)
        add_popup.title("Add New Item")
        add_popup.geometry("300x400")
        add_popup.grab_set()

        tk.Label(add_popup, text="Item Name:").pack(pady=5)
        name_entry = tk.Entry(add_popup)
        name_entry.pack()

        tk.Label(add_popup, text="Item Location:").pack(pady=5)
        location_entry = tk.Entry(add_popup)
        location_entry.pack()

        tk.Label(add_popup, text="Item Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(add_popup)    
        quantity_entry.pack()

        def submit():
            name = name_entry.get()
            location = location_entry.get()
            quantity = quantity_entry.get()
            
            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity must be a number between 0 and 9999.")
                return
            
            if not name or not location or quantity < 0 or quantity > 9999:
                messagebox.showerror("Invalid Input", "Please provide valid item details.")
                return

            new_item = Item(name, location, int(quantity))
            ItemDB().add_item(new_item)

            messagebox.showinfo("Success", f"Item '{name}' added successfully.")
            add_popup.destroy()
            self.refresh_table()

        tk.Button(add_popup, text="Submit", command=submit, bg="green", fg="white").pack(pady=20)



class StockPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller
        controller.title("Stock Monitor")


        #HEADER - inc back, title, and logout buttons
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="Stock Monitor") 
        self.title_label.grid(row=0, column=1)#centre

    def back(self):
        self.controller.show_frame("DashboardPage")

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller
        controller.title("Admin Settings")


        #HEADER - inc back, title, and logout buttons
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="Admin Settings")
        self.title_label.grid(row=0, column=1)#centre

    def back(self):
        self.controller.show_frame("DashboardPage")


if __name__ == "__main__":
    app = App()
    app.mainloop()  