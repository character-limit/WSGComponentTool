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

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (LoginPage, DashboardPage):
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

        tk.Label(self, text="Password").pack()
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

        label = tk.Label(self, text="Dashboard", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Go to Login Page", command=lambda:controller.show_frame("LoginPage"))
        button1.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()  