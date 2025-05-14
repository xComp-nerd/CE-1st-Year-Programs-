''' Source code authored by Allen Penano and Arjohn Laurio'''

import tkinter as tk
from tkinter import ttk, messagebox
import time
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def get_vehicle_type(self): pass
    @abstractmethod
    def get_id(self): pass
    @abstractmethod
    def get_brand(self): pass
    @abstractmethod
    def get_model(self): pass
    @abstractmethod
    def get_status(self): pass
    @abstractmethod
    def is_visible(self): pass
    @abstractmethod
    def set_visible(self, flag: bool): pass
    @abstractmethod
    def get_time(self): pass
    @abstractmethod
    def get_cost(self): pass
    @abstractmethod
    def get_cost_description(self): pass
    @abstractmethod
    def get_tracker(self): pass
    @abstractmethod
    def get_username(self): pass
    @abstractmethod
    def clear_username(self): pass

class Tracker:
    def __init__(self):
        self.start_ts = None
        self.end_ts = None

    def start_rent(self):
        self.start_ts = time.time()

    def end_rent(self):
        self.end_ts = time.time()

    def elapsed_units(self, seconds_per_unit):
        if not (self.start_ts and self.end_ts):
            return 0
        return (self.end_ts - self.start_ts) / seconds_per_unit

class Bicycle(Vehicle):
    def __init__(self, vid, brand, model, cost, cost_desc, time_unit):
        self._type = "Bicycle"
        self._id = vid
        self._brand = brand
        self._model = model
        self._status = "Available"
        self._visible = True
        self._tracker = Tracker()
        self._username = ["", ""]
        self._cost = cost
        self._cost_desc = cost_desc
        self._time_unit = time_unit

    def get_vehicle_type(self): return self._type
    def get_id(self): return self._id
    def get_brand(self): return self._brand
    def get_model(self): return self._model
    def get_status(self): return self._status
    def is_visible(self): return self._visible
    def set_visible(self, flag: bool): self._visible = flag
    def get_time(self): return self._time_unit
    def get_cost(self): return self._cost
    def get_cost_description(self): return self._cost_desc
    def get_tracker(self): return self._tracker
    def get_username(self): return self._username
    def set_status(self, status): self._status = status
    def clear_username(self):
        self._username[0] = ""
        self._username[1] = ""

class Motorcycle(Vehicle):
    def __init__(self, vid, brand, model, cost, cost_desc, time_unit):
        self._type = "Motorcycle"
        self._id = vid
        self._brand = brand
        self._model = model
        self._status = "Available"
        self._visible = True
        self._tracker = Tracker()
        self._username = ["", ""]
        self._cost = cost
        self._cost_desc = cost_desc
        self._time_unit = time_unit

    def get_vehicle_type(self): return self._type
    def get_id(self): return self._id
    def get_brand(self): return self._brand
    def get_model(self): return self._model
    def get_status(self): return self._status
    def is_visible(self): return self._visible
    def set_visible(self, flag: bool): self._visible = flag
    def get_time(self): return self._time_unit
    def get_cost(self): return self._cost
    def get_cost_description(self): return self._cost_desc
    def get_tracker(self): return self._tracker
    def get_username(self): return self._username
    def set_status(self, status): self._status = status
    def clear_username(self):
        self._username[0] = ""
        self._username[1] = ""

class Car(Vehicle):
    def __init__(self, vid, brand, model, cost, cost_desc, time_unit):
        self._type = "Car"
        self._id = vid
        self._brand = brand
        self._model = model
        self._status = "Available"
        self._visible = True
        self._tracker = Tracker()
        self._username = ["", ""]
        self._cost = cost
        self._cost_desc = cost_desc
        self._time_unit = time_unit

    def get_vehicle_type(self): return self._type
    def get_id(self): return self._id
    def get_brand(self): return self._brand
    def get_model(self): return self._model
    def get_status(self): return self._status
    def is_visible(self): return self._visible
    def set_visible(self, flag: bool): self._visible = flag
    def get_time(self): return self._time_unit
    def get_cost(self): return self._cost
    def get_cost_description(self): return self._cost_desc
    def get_tracker(self): return self._tracker
    def get_username(self): return self._username
    def set_status(self, status): self._status = status
    def clear_username(self):
        self._username[0] = ""
        self._username[1] = ""

class Truck(Vehicle):
    def __init__(self, vid, brand, model, cost, cost_desc, time_unit):
        self._type = "Truck"
        self._id = vid
        self._brand = brand
        self._model = model
        self._status = "Available"
        self._visible = True
        self._tracker = Tracker()
        self._username = ["", ""]
        self._cost = cost
        self._cost_desc = cost_desc
        self._time_unit = time_unit

    def get_vehicle_type(self): return self._type
    def get_id(self): return self._id
    def get_brand(self): return self._brand
    def get_model(self): return self._model
    def get_status(self): return self._status
    def is_visible(self): return self._visible
    def set_visible(self, flag: bool): self._visible = flag
    def get_time(self): return self._time_unit
    def get_cost(self): return self._cost
    def get_cost_description(self): return self._cost_desc
    def get_tracker(self): return self._tracker
    def get_username(self): return self._username
    def set_status(self, status): self._status = status
    def clear_username(self):
        self._username[0] = ""
        self._username[1] = ""


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Vehicle Rental System")
        self.root.geometry("900x600")
        self.panel = "dashboard"
        self.chosen_vehicle = None
        self.registered_usernames = set()

        self.available_vehicles = [
            Bicycle("B001", "Trek", "FX 1", 70, "per hour", 3600),
            Motorcycle("M001", "XRM", "HONDA", 150, "per hour", 3600),
            Car("C001", "L300", "SUZUKI", 1000, "per day", 84600),
            Truck("T001", "QKR77 E", "ISUZU", 5000, "per day", 84600),
        ]

        self.Program()
        self.root.mainloop()

    def Program(self):
        for widget in self.root.winfo_children(): widget.destroy()
        top = tk.Frame(self.root, bg='grey', height=50)
        top.pack(fill='x')
        tk.Label(top, text="Vehicle Rental System", font=("Helvetica",18,"bold"), fg='white', bg='grey').pack(pady=10)
        main = tk.Frame(self.root, bg='lightgrey')
        main.pack(fill='both', expand=True)
        if self.panel == "dashboard":
            self.build_dashboard(main)
        elif self.panel == "detail":
            self.build_detail(main)
        elif self.panel == "rented":
            self.build_rented(main)
        elif self.panel == "billing":
            self.build_billing(main)

    def build_dashboard(self, main):
        left = tk.Frame(main, bg='white', bd=2, relief='groove')
        left.pack(side='left', fill='y', padx=10, pady=10)
        tk.Label(left, text="Search Vehicle", font=("Arial",14,"bold"), bg='white').pack(pady=(10,5))
        tk.Label(left, text="Type:", bg='white').pack(anchor='w', padx=10)
        types = list({v.get_vehicle_type() for v in self.available_vehicles})
        self.search_cb = ttk.Combobox(left, values=types)
        self.search_cb.pack(fill='x', padx=10, pady=(0,10))
        ttk.Button(left, text="Search", command=self.search_vehicle).pack(fill='x', padx=10)
        ttk.Button(left, text="Reset", command=self.reset_search).pack(fill='x', padx=10, pady=5)

        right = tk.Frame(main, bg='white', bd=2, relief='groove')
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        tk.Label(right, text="Available Vehicles", font=("Arial",14,"bold"), bg='white').pack(pady=10)
        cols = ("Type","ID","Brand","Model","Status")
        self.tree = ttk.Treeview(right, columns=cols, show='headings', height=12)
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=100)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.pack(fill='both', expand=True, padx=10, pady=(0,10))
        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for v in self.available_vehicles:
            if v.is_visible():
                self.tree.insert('', 'end', values=(v.get_vehicle_type(), v.get_id(), v.get_brand(), v.get_model(), v.get_status()))

    def search_vehicle(self):
        term = self.search_cb.get().strip()
        for v in self.available_vehicles: v.set_visible(term=="" or v.get_vehicle_type()==term)
        self.populate_tree()

    def reset_search(self):
        self.search_cb.set("")
        for v in self.available_vehicles: v.set_visible(True)
        self.populate_tree()

    def on_select(self, event):
        vals = self.tree.item(self.tree.focus())['values']
        vid = vals[1]
        for v in self.available_vehicles:
            if v.get_id()==vid:
                self.chosen_vehicle = v
                if v.get_status()=="Rented":
                    self.prompt_login()
                else:
                    self.panel = "detail"
                    self.Program()
                break

    def prompt_login(self):
        v = self.chosen_vehicle
        login_win = tk.Toplevel(self.root)
        login_win.title("Login to Manage Rental")
        login_win.geometry("300x200")
        ttk.Label(login_win, text="Username:").pack(pady=(20,5))
        user_var = tk.StringVar()
        ttk.Entry(login_win, textvariable=user_var).pack()
        ttk.Label(login_win, text="Password:").pack(pady=(10,5))
        pass_var = tk.StringVar()
        ttk.Entry(login_win, textvariable=pass_var, show="*").pack()
        def do_login():
            if user_var.get()==v.get_username()[0] and pass_var.get()==v.get_username()[1]:
                login_win.destroy()
                self.panel = "rented"
                self.Program()
            else:
                messagebox.showerror("Error","Invalid credentials")
        ttk.Button(login_win, text="Login", command=do_login).pack(pady=20)

    def build_detail(self, main):
        v=self.chosen_vehicle
        ttk.Button(self.root, text="< Back", command=self.go_dashboard).place(x=10,y=60)
        frame=tk.Frame(main,bg='white',bd=2,relief='ridge'); frame.pack(fill='both',expand=True,padx=10,pady=10)
        tk.Label(frame,text=f"{v.get_vehicle_type()} Details",font=("Arial",16,"bold"),bg='white',fg='darkgreen').pack(pady=10)
        for lbl,val in [("ID",v.get_id()),("Brand",v.get_brand()),("Model",v.get_model()),("Status",v.get_status()),("Cost",f"₱{v.get_cost()}/{v.get_cost_description()}")]:
            tk.Label(frame,text=f"{lbl}: {val}",bg='white').pack(anchor='w',padx=20,pady=2)
        rent=tk.Frame(frame,bg='white'); rent.pack(pady=20)
        tk.Label(rent,text="Username:",bg='white').grid(row=0,column=0,sticky='e',padx=5,pady=5)
        self.user_var=tk.StringVar(); tk.Entry(rent,textvariable=self.user_var).grid(row=0,column=1,padx=5,pady=5)
        tk.Label(rent,text="Password:",bg='white').grid(row=1,column=0,sticky='e',padx=5,pady=5)
        self.pw_var=tk.StringVar(); tk.Entry(rent,textvariable=self.pw_var,show="*").grid(row=1,column=1,padx=5,pady=5)
        ttk.Button(frame,text="Rent Vehicle",command=self.rent_vehicle).pack(pady=10)

    def rent_vehicle(self):
        u,p=self.user_var.get().strip(),self.pw_var.get().strip()
        if not(u and p): messagebox.showerror("Error","Enter username/password"); return
        if u in self.registered_usernames: messagebox.showerror("Error","Username already registered"); return
        v=self.chosen_vehicle; v.get_username()[0]=u; v.get_username()[1]=p; v.set_status("Rented"); v.get_tracker().start_rent()
        self.registered_usernames.add(u)
        self.panel="rented"; self.Program()

    def build_rented(self, main):
        ttk.Button(self.root,text="< Back",command=self.go_dashboard).place(x=10,y=60)
        tk.Label(main,text="Rented Vehicle Details",font=("Arial",16,"bold"),bg='white').pack(pady=20)
        ttk.Button(main,text="End Rent",command=self.end_rent).pack()

    def end_rent(self):
        v = self.chosen_vehicle
        prev_user = v.get_username()[0]
        v.get_tracker().end_rent()
        v.clear_username()
        v.set_status("Available")
        self.registered_usernames.discard(prev_user)
        self.panel="billing"
        self.Program()

    def build_billing(self, main):
        v=self.chosen_vehicle; t=v.get_tracker(); unit=v.get_time(); cost=v.get_cost()
        secs=t.end_ts - t.start_ts; units=round(secs/unit,2); amt=round(units*cost,2)
        ttk.Button(self.root,text="< Back",command=self.go_dashboard).place(x=10,y=60)
        f=tk.Frame(main,bg='white',bd=2,relief='groove'); f.pack(padx=20,pady=20,fill='both',expand=True)
        tk.Label(f,text="Billing Summary",font=("Arial",16,"bold"),bg='white').pack(pady=10)
        info=[("Type",v.get_vehicle_type()),("ID",v.get_id()),("Brand",v.get_brand()),("Model",v.get_model()),("Rate",f"₱{cost} per {v.get_cost_description()}")]
        for lbl,val in info: tk.Label(f,text=f"{lbl}: {val}",bg='white').pack(anchor='w',padx=20,pady=2)
        tk.Label(f,text=f"Start: {time.ctime(t.start_ts)}",bg='white').pack(anchor='w',padx=20)
        tk.Label(f,text=f"End: {time.ctime(t.end_ts)}",bg='white').pack(anchor='w',padx=20)
        tk.Label(f,text=f"Duration: {round(secs,2)} seconds ({units} units)",bg='white').pack(anchor='w',padx=20,pady=(10,0))
        tk.Label(f,text=f"Calculation: {units} × ₱{cost} = ₱{amt}",bg='white',fg='green').pack(anchor='w',padx=20)
        tk.Label(f,text=f"Amount Due: ₱{amt}",font=("Arial",14),bg='white',fg='green').pack(pady=20)
        ttk.Button(f,text="Exit",command=self.root.quit).pack()

    def go_dashboard(self): self.panel="dashboard"; self.Program()

if __name__== "__main__":
    Main()