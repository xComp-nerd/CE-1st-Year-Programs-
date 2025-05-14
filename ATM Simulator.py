''' Source code authored by Ronyn Escalera and Kevin Aniete'''

import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class ATMInterface(ABC):
    @abstractmethod
    def start(self):
        """Abstract method to start the ATM simulator."""
        pass

class ATMSimulator(ATMInterface):
    def __init__(self, master):
        self.master = master
        self.master.title("ATM Simulator")
        self.master.geometry("400x350")
        # In-memory account storage: PIN -> balance
        self.accounts = {}
        self.current_pin = None

        # Frames
        self.start_frame = tk.Frame(self.master)
        self.login_frame = tk.Frame(self.master)
        self.create_frame = tk.Frame(self.master)
        self.menu_frame = tk.Frame(self.master)

        self.create_start_frame()

    def create_start_frame(self):
        self.clear_frame(self.login_frame)
        self.clear_frame(self.create_frame)
        self.clear_frame(self.menu_frame)
        self.start_frame.pack(pady=60)

        tk.Label(self.start_frame, text="Welcome to ATM Simulator", font=(None, 16)).pack(pady=10)
        tk.Button(
            self.start_frame,
            text="Login to Existing Account",
            width=25,
            command=self.create_login_frame
        ).pack(pady=5)
        tk.Button(
            self.start_frame,
            text="Create New Account",
            width=25,
            command=self.create_account_frame
        ).pack(pady=5)

    def create_login_frame(self):
        self.clear_frame(self.start_frame)
        self.clear_frame(self.create_frame)
        self.login_frame.pack(pady=50)

        tk.Label(self.login_frame, text="Enter PIN:").grid(row=0, column=0, pady=5)
        self.pin_entry = tk.Entry(self.login_frame, show="*")
        self.pin_entry.grid(row=0, column=1, pady=5)

        tk.Button(
            self.login_frame,
            text="Login",
            width=10,
            command=self.check_pin
        ).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(
            self.login_frame,
            text="Back",
            width=10,
            command=self.create_start_frame
        ).grid(row=2, column=0, columnspan=2)

    def create_account_frame(self):
        self.clear_frame(self.start_frame)
        self.clear_frame(self.login_frame)
        self.create_frame.pack(pady=30)

        tk.Label(self.create_frame, text="Set a 4-digit PIN:").grid(row=0, column=0, pady=5)
        self.new_pin_entry = tk.Entry(self.create_frame, show="*")
        self.new_pin_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.create_frame, text="Initial Deposit:").grid(row=1, column=0, pady=5)
        self.init_deposit_entry = tk.Entry(self.create_frame)
        self.init_deposit_entry.grid(row=1, column=1, pady=5)

        tk.Button(
            self.create_frame,
            text="Create",
            width=10,
            command=self.create_account
        ).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(
            self.create_frame,
            text="Back",
            width=10,
            command=self.create_start_frame
        ).grid(row=3, column=0, columnspan=2)

    def create_account(self):
        pin = self.new_pin_entry.get().strip()
        deposit = self.init_deposit_entry.get().strip()
        # Validate PIN and deposit
        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be exactly 4 digits.")
            return
        if pin in self.accounts:
            messagebox.showerror("Error", "An account with that PIN already exists.")
            return
        try:
            amount = float(deposit)
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid non-negative deposit.")
            return
        # Create account
        self.accounts[pin] = amount
        messagebox.showinfo("Success", f"Account created with balance ${amount:.2f}.")
        self.clear_frame(self.create_frame)
        self.create_login_frame()

    def create_menu_frame(self):
        self.clear_frame(self.login_frame)
        self.clear_frame(self.start_frame)
        self.menu_frame.pack(pady=30)

        balance = self.accounts.get(self.current_pin, 0.0)
        tk.Label(
            self.menu_frame,
            text=f"Balance: ${balance:.2f}",
            font=(None, 14)
        ).pack(pady=10)
        tk.Button(
            self.menu_frame,
            text="Deposit",
            width=15,
            command=self.deposit_window
        ).pack(pady=5)
        tk.Button(
            self.menu_frame,
            text="Withdraw",
            width=15,
            command=self.withdraw_window
        ).pack(pady=5)
        tk.Button(
            self.menu_frame,
            text="Logout",
            width=15,
            command=self.exit_session
        ).pack(pady=5)

    def check_pin(self):
        entered_pin = self.pin_entry.get().strip()
        # Check if PIN exists
        if entered_pin in self.accounts:
            self.pin_entry.delete(0, tk.END)
            self.current_pin = entered_pin
            self.create_menu_frame()
        else:
            messagebox.showerror("Error", "Invalid PIN. Try again.")
            self.pin_entry.delete(0, tk.END)

    def deposit_window(self):
        self.transaction_window("Deposit", self.perform_deposit)

    def withdraw_window(self):
        self.transaction_window("Withdraw", self.perform_withdraw)

    def transaction_window(self, title, action):
        win = tk.Toplevel(self.master)
        win.title(title)
        win.geometry("300x150")

        tk.Label(win, text=f"Enter amount to {title.lower()}:").pack(pady=10)
        amount_entry = tk.Entry(win)
        amount_entry.pack(pady=5)

        def on_confirm():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError
                action(amount)
                win.destroy()
                self.refresh_balance()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid positive number.")

        tk.Button(win, text="Confirm", command=on_confirm).pack(pady=10)

    def perform_deposit(self, amount):
        self.accounts[self.current_pin] += amount
        messagebox.showinfo("Success", f"Deposited ${amount:.2f}.")

    def perform_withdraw(self, amount):
        if amount > self.accounts[self.current_pin]:
            messagebox.showerror("Error", "Insufficient funds.")
        else:
            self.accounts[self.current_pin] -= amount
            messagebox.showinfo("Success", f"Withdrew ${amount:.2f}.")

    def refresh_balance(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        self.create_menu_frame()

    def exit_session(self):
        self.clear_frame(self.menu_frame)
        self.current_pin = None
        messagebox.showinfo("Goodbye", "You have been logged out.")
        self.create_start_frame()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack_forget()

    def start(self):
        """Implementation of abstract start method."""
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMSimulator(root)
    app.start()