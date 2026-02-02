import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from audit import Audit
import audit
from auditdb import AuditDB
from user import User
from userdb import UserDB
from item import Item
from itemdb import ItemDB
import datetime
""" Class to manage the GUI application """
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

        for F in (LoginPage, DashboardPage, InventoryPage, StockPage, AdminPage, UserManagePage, AuditPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

""" Class to hold the login page and its associated methods """
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
        if UserDB().check_login(username, password) == 1:
            self.controller.show_frame("DashboardPage")
        elif UserDB().check_login(username, password) == 0:
            messagebox.showerror("Login Failed", "Invalid username or password.")
        elif UserDB().check_login(username, password) == -1:
            messagebox.showerror("Account Locked", "Your account has been irreversibly locked. Please contact the system administrator for more information.")

""" Class to hold the dashboard page and its associated methods """
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

    #method for then logout button is pressed
    def logout(self):
        self.controller.show_frame("LoginPage")

    #method for when inventory button is pressed
    def open_inventory(self):
        self.controller.show_frame("InventoryPage")

    #method for when stock monitor button is pressed
    def open_stock_monitor(self):
        self.controller.show_frame("StockPage")
    
    #method for when admin settings button is pressed
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

""" Class to hold the inventory management page and its associated methods """
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

        btn_alert = tk.Button(buttons_frame, text="Create Stock Alert for Selected Item", command=self.createAlert)
        btn_alert.grid(row=0, column=3, sticky="w", padx=5)#left

    #manage back button pressed.
    def back(self):
        self.controller.show_frame("DashboardPage")

    #method to manage searches
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

    #method to delete items.
    def deleteItem(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item)["values"][3]#get id
            item_name = self.tree.item(selected_item)["values"][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?")
            if confirm:
                #CREATE AUDIT FOR Deleting ITEM.
                templog = Audit(f"Deleted item: {item_name} - ID: {item_id}", 
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                User.session.UID
                                )
                
                #SAVE AUDIT
                AuditDB().add_audit(templog)
                ItemDB().remove_item(item_id)
                self.refresh_table()
        else:
            messagebox.showwarning("No Selection", "Please select an item to delete.")

    #method to edit items.
    def editItem(self):
        def submit():
            #get entiries from fields.
            name = name_entry.get()
            location = location_entry.get()
            quantity = quantity_entry.get()
            
            #validation
            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity must be a number between 0 and 9999.")
                return
            
            if not name or not location or quantity < 0 or quantity > 9999:
                messagebox.showerror("Invalid Input", "Please provide valid item details.")
                return

            #CREATE AUDIT FOR Editing ITEM.
            templog = Audit(f"Edited item: {selected.name} - ID: {selected.ID}. Old Values - Name: {selected.name}, Location: {selected.location}, Quantity: {selected.quantity}. New Values - Name: {name}, Location: {location}, Quantity: {quantity}", 
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                            User.session.UID
                            )
            
            #SAVE AUDIT
            AuditDB().add_audit(templog)
            selected.name = name
            selected.location = location
            selected.quantity = int(quantity)
            ItemDB().edit_item(selected)
            messagebox.showinfo("Success", f"Item '{selected.name}' edited successfully.")
            add_popup.destroy()
            self.refresh_table()

        #get selected item
        selected_item = self.tree.selection()
        if selected_item: #validate an item is selected
            item_id = self.tree.item(selected_item)["values"][3]#get id
            selected = ItemDB().get_item(item_id)#get item

            #popup to edit item
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

            tk.Button(add_popup, text="Submit", command=submit, bg="green", fg="white").pack(pady=20)
        else:
            messagebox.showwarning("No Selection", "Please select an item to edit.")

    def createAlert(self):
        
        def submit(): #submit button press for creating alert.
            low_quantity = low_quantity_entry.get() #get low stock threshold from entry field.
            
            #Validation. 
            try:
                low_quantity = int(low_quantity)#Try to parse to int, for type check.
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity must be a number between 0 and 9999.") #error message if type check fails.
                return
            
            if  low_quantity < 0 or low_quantity > 9999: #range check quantity is between 0 and 9999
                messagebox.showerror("Invalid Input", "Quantity must be a number between 0 and 9999.") #error message if range check fails.
                return

            #CREATE AUDIT FOR ADDING ITEM.
            templog = Audit(f"Edited low stock alert for item: {selected.name}, New Threshold: {low_quantity}, Old Threshold: {selected.minQuantity}", 
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #get current timestamp
                            User.session.UID    #get current userID (FK for audit log)
                            )
            
            #SAVE AUDIT
            AuditDB().add_audit(templog)

            selected.minQuantity = low_quantity #set new stock alert threshold
            ItemDB().edit_item(selected)
            messagebox.showinfo("Success", f"Low stock alert created for item '{selected.name}'!")
            add_popup.destroy()
            self.refresh_table()


        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item)["values"][3]#get id
            selected = ItemDB().get_item(item_id)#get item

            #pu
            add_popup = tk.Toplevel(self)
            add_popup.title(f"Create Stock Alert - {selected.name}, Current Qty: {selected.quantity}")
            add_popup.geometry("300x400")
            add_popup.grab_set()

            tk.Label(add_popup, text="Low Stock Alert Quantity:").pack(pady=5)
            low_quantity_entry = tk.Entry(add_popup)    
            low_quantity_entry.pack()

            tk.Button(add_popup, text="Create Low Stock Alert", command=submit, bg="green", fg="white").pack(pady=20)
        else:
            messagebox.showwarning("No Selection", "Please select an item to create an alert.")

    def refresh_table(self):
        self.search_entry.delete(0, tk.END)#clear search bar

        for row in self.tree.get_children():
            self.tree.delete(row)#clear all rows
        
        items = ItemDB().get_items("")  #get all items

        if items:
            for item in items:
                self.tree.insert("", tk.END, values=(item.name, item.quantity, item.location, item.ID))

    #refresh table upon opening page.
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

            #CREATE AUDIT FOR ADDING ITEM.
            templog = Audit(f"Added new item: {name}, Location: {location}, Quantity: {quantity}", 
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                            User.session.UID
                            )
            
            #SAVE AUDIT
            AuditDB().add_audit(templog)

            messagebox.showinfo("Success", f"Item '{name}' added successfully.")
            add_popup.destroy()
            self.refresh_table()

        tk.Button(add_popup, text="Submit", command=submit, bg="green", fg="white").pack(pady=20)

class StockPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.low_stock_only = tk.BooleanVar()

        #set self controller for use in methods
        self.controller = controller
        controller.title("Stock Monitor")

        #HEADER - inc back, title
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="Stock Monitor")
        self.title_label.grid(row=0, column=1)#centre

        #Restock radio check  
        search_frame = tk.Frame(self)
        search_frame.pack(side="top", fill="x", padx=10, pady=5)

        self.low_only = tk.Checkbutton(search_frame, text="Show Low Stock Only", variable=self.low_stock_only, command=self.refresh_table)
        self.low_only.pack(pady=5,anchor="w")

        #TABLE
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Columns = ["Name", "Quantity", "Threshold", "Location", "Item ID"]
        self.tree = ttk.Treeview(table_frame, columns=Columns, show="headings")

        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Threshold", text="Threshold")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Item ID", text="Item ID")

        self.tree.column("Name", width=250, anchor="center")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Threshold", width=100, anchor="center")
        self.tree.column("Location", width=150, anchor="center")
        self.tree.column("Item ID", width=100, anchor="center")

        scollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scollbar.pack(side="right", fill="y")

    def back(self):
        self.controller.show_frame("DashboardPage")
    
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)#clear all rows

        items = ItemDB().get_items_monitoring(self.low_stock_only.get())  #get items, low stock only if checked on gui

        if items:
            for item in items:
                self.tree.insert("", tk.END, values=(item.name, item.quantity, item.minQuantity, item.location, item.ID))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_table()

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

        self.title_label = tk.Label(head_frame, text="Admin Dashboard")
        self.title_label.grid(row=0, column=1)#centre

        #MENU BUTTONS - manage users, audit logs
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_inventory = tk.Button(center_frame, text="Manage\nUsers", width=30, height=13, command=self.open_users)
        btn_inventory.grid(row=0, column=0, padx=10)

        btn_stock = tk.Button(center_frame, text="Audit\nLogs", width=30, height=13, command=self.open_audit)
        btn_stock.grid(row=0, column=1, padx=10)

    def back(self):
        self.controller.show_frame("DashboardPage")

    def open_users(self):
        self.controller.show_frame("UserManagePage")

    def open_audit(self):
        self.controller.show_frame("AuditPage")

    
    #update elements when frame is raised
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)

        self.title_label.config(text=f"Dashboard - {User.session.username}") #update username when raising frame

        """ if User.session.isAdmin == True:
            self.btn_admin.config(state="normal")
        else:
            self.btn_admin.config(state="disabled") """

class UserManagePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller
        controller.title("User Management")

        #HEADER - inc back, title, and logout buttons
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="User Management")
        self.title_label.grid(row=0, column=1)#centre

        #TABLE
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Columns = ["Username", "Name", "Admin"]
        self.tree = ttk.Treeview(table_frame, columns=Columns, show="headings")

        self.tree.heading("Username", text="Username")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Admin", text="Admin")

        self.tree.column("Username", width=200, anchor="center")
        self.tree.column("Name", width=200, anchor="center")
        self.tree.column("Admin", width=50, anchor="center")

        scollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scollbar.pack(side="right", fill="y")

        #bottom buttons (add user, promote to admin, demote, lock account)
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side="bottom", fill="x", padx=10, pady=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        btn_create = tk.Button(buttons_frame, text="Create User", command=self.createUser)
        btn_create.grid(row=0, column=0, sticky="w", padx=5)#left

        btn_lock = tk.Button(buttons_frame, text="Lock Account", command=self.lockUser)
        btn_lock.grid(row=0, column=1, sticky="w", padx=5)#left

        btn_promote = tk.Button(buttons_frame, text="Promote (Admin)", command=self.promoteUser)
        btn_promote.grid(row=0, column=2, sticky="w", padx=5)#left

        btn_demote = tk.Button(buttons_frame, text="Demote (User)", command=self.demoteUser)
        btn_demote.grid(row=0, column=3, sticky="w", padx=5)#left

    def back(self):
        self.controller.show_frame("AdminPage")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row) # clear all rows

        users = UserDB().get_users()  #get all users

        if users:
            for user in users:
                self.tree.insert("", tk.END, values=(user.username, user.firstName + " " + user.lastName, user.isAdmin))

    #refresh table upon opening page.
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_table()

    def createUser(self):
        #popup
        add_popup = tk.Toplevel(self)
        add_popup.title("Create User")
        add_popup.geometry("300x400")
        add_popup.grab_set()

        tk.Label(add_popup, text="First Name:").pack(pady=5)
        first_name_entry = tk.Entry(add_popup)    
        first_name_entry.pack()

        tk.Label(add_popup, text="Last Name:").pack(pady=5)
        last_name_entry = tk.Entry(add_popup)    
        last_name_entry.pack()

        tk.Label(add_popup, text="Username:").pack(pady=5)
        username_entry = tk.Entry(add_popup)
        username_entry.pack()

        tk.Label(add_popup, text="Password:").pack(pady=5)
        password_entry = tk.Entry(add_popup)
        password_entry.pack()

        def submit():
            #get entries from fields.
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            
            try:
                #validate they are of type string using try catch in type conversion.
                username = str(username)
                password = str(password)
            except ValueError:
                messagebox.showerror("Invalid Input", "Username or Password must be valid.") #error message if wrong type provided.
                return

            #validate lengths. firstname and last name presence check.
            if len(username) < 3 or not first_name or not last_name or len(password) < 8: #show error message if range/presence check fails. 
                messagebox.showerror("Invalid Input", "Please provide valid user. Username must be at least 3 characters and password at least 8 characters.")
                return

            #create user object
            new_user = User(first_name, last_name, username, password)
            UserDB().add_user(new_user) #save new user to db

            messagebox.showinfo("Success", f"User '{username}' created successfully.") #confirmation popup
            add_popup.destroy()
            self.refresh_table()

        tk.Button(add_popup, text="Submit", command=submit, bg="green", fg="white").pack(pady=20)

    def lockUser(self):
        selected_user = self.tree.selection()
        if selected_user:
            username = self.tree.item(selected_user)["values"][0]#get username
            selected = UserDB().get_user(username)#get user

            if not messagebox.askokcancel("Confirm Lock", f"Are you sure you want to lock the account for '{selected.username}'? This action cannot be undone."):
                return

            selected.password = b"lockedlockedlocked!"

            UserDB().edit_user(selected)

            messagebox.showinfo("Success", f"User '{selected.username}' locked successfully.")
            self.refresh_table()
        else:
            messagebox.showwarning("No Selection", "Please select a user to promote.")   

    def promoteUser(self):
        selected_user = self.tree.selection()
        if selected_user:
            username = self.tree.item(selected_user)["values"][0]#get username
            selected = UserDB().get_user(username)#get user

            if selected.isAdmin:
                messagebox.showinfo("Error", f"User '{selected.username}' is already an admin.")
                return

            selected.isAdmin = True

            UserDB().edit_user(selected)

            messagebox.showinfo("Success", f"User '{selected.username}' promoted to admin successfully.")
            self.refresh_table()
        else:
            messagebox.showwarning("No Selection", "Please select a user to promote.")

    def demoteUser(self):
        selected_user = self.tree.selection()
        if selected_user:
            username = self.tree.item(selected_user)["values"][0]#get username
            selected = UserDB().get_user(username)#get user

            if not selected.isAdmin:
                messagebox.showinfo("Error", f"User '{selected.username}' is already demoted.")
                return

            selected.isAdmin = False

            UserDB().edit_user(selected)

            messagebox.showinfo("Success", f"User '{selected.username}' demoted successfully.")
            self.refresh_table()
        else:
            messagebox.showwarning("No Selection", "Please select a user to demote.")

class AuditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #set self controller for use in methods
        self.controller = controller
        controller.title("Audit Logs")

        #HEADER - inc back, title, and logout buttons
        head_frame = tk.Frame(self)
        head_frame.pack(side="top", fill="x", padx=10, pady=1)
        head_frame.grid_columnconfigure(1, weight=1)

        btn_back = tk.Button(head_frame, text="Back", command=self.back)
        btn_back.grid(row=0, column=0, sticky="w")#left

        self.title_label = tk.Label(head_frame, text="Audit Logs")
        self.title_label.grid(row=0, column=1)#centre

        #TABLE
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Columns = ["Action", "Username", "Time"]
        self.tree = ttk.Treeview(table_frame, columns=Columns, show="headings")

        self.tree.heading("Action", text="Action")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Time", text="Time")

        self.tree.column("Action", width=400, anchor="center")
        self.tree.column("Username", width=100, anchor="center")
        self.tree.column("Time", width=100, anchor="center")

        scollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scollbar.pack(side="right", fill="y")

    def back(self):
        self.controller.show_frame("AdminPage")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)#clear all rows

        audits = AuditDB().get_audits()  #get all audits

        if audits:
            for audit in audits:
                self.tree.insert("", tk.END, values=(audit.description, audit.userID, audit.timestamp))

    #refresh table upon opening page.
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_table()

if __name__ == "__main__":
    app = App()
    app.mainloop()  