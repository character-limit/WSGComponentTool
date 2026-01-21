import tkinter as tk
from tkinter import messagebox
from user import User
from userdb import UserDB


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

    def back(self):
        self.controller.show_frame("DashboardPage")


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