''' Source code authored by Jerrome Galang and none-member Jessa Soriano'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class HospitalManagementSystem:
    def __init__(self):
        self.start()

    patient_record_data = [
        (1, "John Doe", 45, "Male", "555-1234", "Flu", 101),
        (2, "Jane Smith", 30, "Female", "555-5678", "Cold", 102),
        (3, "Michael Brown", 60, "Male", "555-8765", "Diabetes", 104),
        (4, "Emily Davis", 25, "Female", "555-4321", "Asthma", 103),
    ]

    doctor_schedule = [
        (1, "Dr. Alice", "Cardiology", "Mon-Fri 9AM-3PM"),
        (2, "Dr. Bob", "Neurology", "Tue-Thu 10AM-4PM"),
    ]

    room_bed_data = [
        [101, "Single", "Available", ""],
        [102, "Double", "Available", ""],
        [103, "Single", "Available", ""],
        [104, "ICU", "Occupied", ""],
    ]

    def start(self):
        if tk._default_root is not None:
            for window in tk._default_root.winfo_children():
                window.destroy()
            tk._default_root.destroy()
        self.root = tk.Tk()
        self.root.title("Hospital Management System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        title = tk.Label(self.root, text="🏥 Hospital Management System", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=20)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Manage Patients", width=25, height=2, bg="#3498db", fg="white", command=self.open_patient_window).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Doctor Schedules", width=25, height=2, bg="#27ae60", fg="white", command=self.manage_doctors).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Rooms/Beds", width=25, height=2, bg="#f39c12", fg="white", command=self.room_management).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Billing", width=25, height=2, bg="#8e44ad", fg="white", command=self.manage_billing).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Generate Report", width=25, height=2, bg="#8e44ad", fg="white", command=self.report_generation).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Exit", width=25, height=2, bg="#e74c3c", fg="white", command=self.exit_app).grid(row=5, column=0, padx=10, pady=10)
        self.root.mainloop()

    def open_patient_window(self):
        for window in tk._default_root.winfo_children():
            window.destroy()
        tk._default_root.destroy()
        patient_window = tk.Tk()
        patient_window.title("Patient List")
        patient_window.geometry("700x400")
        patient_window.configure(bg="#ffffff")

        title = tk.Label(patient_window, text="👨‍⚕️ List of Patients", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#2c3e50")
        title.pack(pady=10)

        button_frame = tk.Frame(patient_window, bg="#ffffff")
        button_frame.pack(fill='x', pady=10)

        back_button = tk.Button(button_frame, text="Back", command=self.start, bg="#3498db", fg="white", width=10)
        back_button.pack(side='left', padx=10)

        tree_frame = tk.Frame(patient_window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Name", "Age", "Gender", "Contact", "Diagnosis", "Room ID")
        self.patient_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set, height=10)
        self.patient_tree.pack()

        tree_scroll.config(command=self.patient_tree.yview)

        for patient in self.patient_record_data:
            for room in self.room_bed_data:
                if patient[6] == room[0]:
                    room[2] = "Occupied"       # mark *this* room as occupied
                    room[3] = patient[1]       # store the patient’s name

        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=100)

        for patient in self.patient_record_data:
            self.patient_tree.insert("", tk.END, values=patient)

        action_frame = tk.Frame(patient_window, bg="#ffffff")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Add", command=self.add_patient_record, width=10, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Edit", command=lambda: self.edit_patient_record(self.patient_tree.item(self.patient_tree.selection())), width=10, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Dismiss", command=lambda: self.delete_record(self.patient_tree.item(self.patient_tree.selection())), width=10, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)

    def edit_patient_record(self, patient_record):
        if not patient_record['values']:
            return
        for window in tk._default_root.winfo_children():
            window.destroy()
        tk._default_root.destroy()
        self.patient_record = patient_record['values']
        patient_data = {
            "Name": self.patient_record[1],
            "Age": self.patient_record[2],
            "Gender": self.patient_record[3],
            "Contact": self.patient_record[4],
            "Diagnosis": self.patient_record[5],
            "Room ID": self.patient_record[6]
        }


        edit_window = tk.Tk()
        edit_window.title("Edit Patient Record")
        edit_window.geometry("400x400")
        edit_window.configure(bg="#ffffff")

        button_frame = tk.Frame(edit_window, bg="#ffffff")
        button_frame.pack(fill='x', pady=10)

        back_button = tk.Button(button_frame, text="Back", command=self.open_patient_window, bg="#3498db", fg="white", width=10)
        back_button.pack(side='left', padx=10)

        tk.Label(edit_window, text="Edit Patient Record", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        form_frame = tk.Frame(edit_window, bg="#ffffff")
        form_frame.pack(pady=10)

        labels = ["Name", "Age", "Gender", "Contact", "Diagnosis", "Room ID"]
        changed_records = {}

        # Only show currently available rooms
        available_rooms = [room[0] for room in self.room_bed_data if room[2] == "Available"]
        # Include patient's current room
        if patient_data["Room ID"] not in available_rooms:
            available_rooms.append(patient_data["Room ID"])

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#ffffff", anchor="w", width=10).grid(row=i, column=0, padx=10, pady=5)
            if label == "Room ID":
                cb = ttk.Combobox(form_frame, values=available_rooms, width=28)
                cb.set(patient_data["Room ID"] if patient_data["Room ID"] else "")
                cb.grid(row=i, column=1, padx=10, pady=5)
                changed_records[label] = cb
            else:
                entry = tk.Entry(form_frame, width=30)
                entry.insert(0, patient_data[label])
                entry.grid(row=i, column=1, padx=10, pady=5)
                changed_records[label] = entry

        save_button = tk.Button(edit_window, text="Save Changes", command=lambda: self.patient_record_edit_save(changed_records), bg="#27ae60", fg="white", font=("Helvetica", 12), width=20, height=2)
        save_button.pack(pady=20)

    def add_patient_record(self):
        add_window = tk.Tk()
        add_window.title("Add New Patient")
        add_window.geometry("400x400")
        add_window.configure(bg="#ffffff")

        labels = ["Name", "Age", "Gender", "Contact", "Diagnosis", "Room ID"]

        tk.Label(add_window, text="Add New Patient", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        form_frame = tk.Frame(add_window, bg="#ffffff")
        form_frame.pack(pady=10)

        entries = {}
        available_rooms = [room[0] for room in self.room_bed_data if room[2] == "Available"]
        available_rooms.sort()

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#ffffff", anchor="w", width=10).grid(row=i, column=0, padx=10, pady=5)
            if label == "Room ID":
                cb = ttk.Combobox(form_frame, values=available_rooms, width=28)
                cb.grid(row=i, column=1, padx=10, pady=5)
                entries[label] = cb
            else:
                entry = tk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[label] = entry

        def save_new_patient():
            new_id = max([rec[0] for rec in self.patient_record_data], default=0) + 1
            try:
                room_val = entries["Room ID"].get()
                new_record = (
                    new_id,
                    entries["Name"].get(),
                    int(entries["Age"].get()),
                   (entries["Gender"].get()),
                   (entries["Contact"].get()),
                   (entries["Diagnosis"].get()),
                    int(room_val) if room_val else None
                )
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data.")
                return

            self.patient_record_data.append(new_record)
            add_window.destroy()
            self.open_patient_window()

        save_button = tk.Button(add_window, text="Add Patient", command=save_new_patient, bg="#27ae60", fg="white", font=("Helvetica", 12), width=20, height=2)
        save_button.pack(pady=20)

    def patient_record_edit_save(self, changed_records):
        updated_fields = {label: widget.get() for label, widget in changed_records.items()}
        patient_id = self.patient_record[0]
        try:
            room_val = int(updated_fields["Room ID"])
        except ValueError:
            room_val = None

        updated_record = (
            patient_id,
            updated_fields["Name"],
            int(updated_fields["Age"]),
            updated_fields["Gender"],
            updated_fields["Contact"],
            updated_fields["Diagnosis"],
            room_val
        )

        for idx, record in enumerate(self.patient_record_data):
            if record[0] == patient_id:
                self.patient_record_data[idx] = updated_record
                break
        self.open_patient_window()
    
    def delete_record(self, patient_record):
        """
        Deletes (dismisses) a patient record and updates room statuses accordingly.
        """
        if patient_record.get('values'):
            patient_id = patient_record['values'][0]
            confirm = messagebox.askyesno("Delete", f"Are you sure you want to dismiss patient ID {patient_id}?")
            if not confirm:
                return

            # Remove patient from records
            self.patient_record_data = [rec for rec in self.patient_record_data if rec[0] != patient_id]

            # Sync room occupancy after deletion
            for room in self.room_bed_data:
                occupants = [p[1] for p in self.patient_record_data if p[6] == room[0]]
                if occupants:
                    room[2] = "Occupied"
                    room[3] = ", ".join(occupants)
                else:
                    room[2] = "Available"
                    room[3] = ""

            # Refresh patient list
            self.open_patient_window()
        else:
            self.open_patient_window()

    
    def manage_doctors(self):
        for window in tk._default_root.winfo_children():
            window.destroy()
        tk._default_root.destroy()
        doc_window = tk.Tk()
        doc_window.title("Manage Doctors")
        doc_window.geometry("600x400")
        doc_window.configure(bg="#ffffff")

        button_frame = tk.Frame(doc_window, bg="#ffffff")
        button_frame.pack(fill='x', pady=10)

        back_button = tk.Button(button_frame, text="Back", command=self.start, bg="#3498db", fg="white", width=10)
        back_button.pack(side='left', padx=10)

        tk.Label(doc_window, text="Doctors Schedule", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        tree_frame = tk.Frame(doc_window)
        tree_frame.pack(pady=10)

        columns = ("ID", "Name", "Specialty", "Schedule")
        doctor_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        doctor_tree.pack()

        for col in columns:
            doctor_tree.heading(col, text=col)
            doctor_tree.column(col, width=120)

        for doctor in self.doctor_schedule:
            doctor_tree.insert("", tk.END, values=doctor)


    def room_management(self):
        # Destroy any existing root windows
        for window in tk._default_root.winfo_children():
            window.destroy()
        tk._default_root.destroy()

        # --- Helper to redraw the table ---
        def refresh_tree():
            for item in room_tree.get_children():
                room_tree.delete(item)
            for room in self.room_bed_data:
                number, rtype = room[0], room[1]
                occupants = [p[1] for p in self.patient_record_data if len(p) > 6 and p[6] == number]
                status = "Occupied" if occupants else "Available"
                names = ", ".join(occupants)
                room_tree.insert("", tk.END, values=(number, rtype, status, names))

        # --- Toggle “Occupied → Available” for a selected room ---
        def toggle_room_status():
            selected = room_tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a room.")
                return
            room_id = room_tree.item(selected[0])['values'][0]

            # Clear assignment from any patient
            new_patients = []
            for pid, name, age, gender, contact, diag, rid in self.patient_record_data:
                if rid == room_id:
                    new_patients.append((pid, name, age, gender, contact, diag, None))
                else:
                    new_patients.append((pid, name, age, gender, contact, diag, rid))
            self.patient_record_data = new_patients

            # Mark room available
            for room in self.room_bed_data:
                if room[0] == room_id:
                    room[2] = "Available"
                    room[3] = ""
            refresh_tree()

        # --- Remove the selected room from the system ---
        def remove_room():
            selected = room_tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a room to remove.")
                return
            room_id = room_tree.item(selected[0])['values'][0]
            confirm = messagebox.askyesno("Remove Room", f"Delete room #{room_id}?")
            if not confirm:
                return

            # Delete from room list
            self.room_bed_data = [r for r in self.room_bed_data if r[0] != room_id]
            # Also clear any patient assignments
            for i, rec in enumerate(self.patient_record_data):
                if rec[6] == room_id:
                    pid, *rest = rec
                    self.patient_record_data[i] = (pid, *rest[:-1], None)
            refresh_tree()

        # --- Add a brand-new room (defaults to Available) ---
        def add_room():
            try:
                new_num = int(new_room_number.get())
                new_type = new_room_type.get().strip()
                if not new_type:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter a valid room number and type.")
                return

            # Prevent duplicates
            if any(r[0] == new_num for r in self.room_bed_data):
                messagebox.showwarning("Duplicate", f"Room #{new_num} already exists.")
                return

            # Append as Available, no occupants
            self.room_bed_data.append([new_num, new_type, "Available", ""])
            new_room_number.delete(0, tk.END)
            new_room_type.delete(0, tk.END)
            refresh_tree()

        # --- Build the window ---
        room_window = tk.Tk()
        room_window.title("Room/Bed Management")
        room_window.geometry("650x400")
        room_window.configure(bg="#ffffff")

        # Back button
        btn_frame = tk.Frame(room_window, bg="#ffffff")
        btn_frame.pack(fill='x', pady=10)
        tk.Button(btn_frame, text="Back", command=self.start, bg="#3498db", fg="white", width=10).pack(side='left', padx=10)

        tk.Label(room_window, text="🛏️ Room/Bed Management", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=5)

        # Table
        columns = ("Room Number", "Type", "Status", "Patients")
        tree_frame = tk.Frame(room_window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        room_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
        room_tree.pack(fill='both', expand=True)
        tree_scroll.config(command=room_tree.yview)
        for col in columns:
            room_tree.heading(col, text=col)
            room_tree.column(col, width=140)
        refresh_tree()

        # Controls: toggle, remove, add
        action_frame = tk.Frame(room_window, bg="#ffffff")
        action_frame.pack(pady=10)

        # Toggle status
        tk.Button(action_frame, text="Toggle Status", command=toggle_room_status,
                bg="#27ae60", fg="white", width=15).grid(row=0, column=0, padx=5)

        # Remove room
        tk.Button(action_frame, text="Remove Room", command=remove_room,
                bg="#e74c3c", fg="white", width=15).grid(row=0, column=1, padx=5)

        # Add room form
        tk.Label(action_frame, text="New #:", bg="#ffffff").grid(row=1, column=0, sticky="e", pady=5)
        new_room_number = tk.Entry(action_frame, width=8)
        new_room_number.grid(row=1, column=1, sticky="w", pady=5)
        tk.Label(action_frame, text="Type:", bg="#ffffff").grid(row=1, column=2, sticky="e", padx=(20,0))
        new_room_type = tk.Entry(action_frame, width=15)
        new_room_type.grid(row=1, column=3, sticky="w", pady=5)
        tk.Button(action_frame, text="Add Room", command=add_room,
                bg="#3498db", fg="white", width=12).grid(row=1, column=4, padx=10)


    def manage_billing(self):
        for window in tk._default_root.winfo_children():
            window.destroy()
        tk._default_root.destroy()

        def calculate_bill():
            selected = patient_tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a patient.")
                return

            item = patient_tree.item(selected)
            values = item['values']
            name = values[1]

            try:
                consultation = float(consultation_entry.get())
                medication = float(medication_entry.get())
                room = float(room_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields.")
                return

            total = consultation + medication + room
            messagebox.showinfo("Billing Summary", f"Patient: {name}\nTotal Bill: ${total:.2f}")

        billing_window = tk.Tk()
        billing_window.title("Billing Management")
        billing_window.geometry("700x400")
        billing_window.configure(bg="#ffffff")

        tk.Label(billing_window, text="💳 Billing Management", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Patient List
        columns = ("ID", "Name", "Age", "Gender", "Contact", "Diagnosis")
        tree_frame = tk.Frame(billing_window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        patient_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set, height=6)
        patient_tree.pack()
        tree_scroll.config(command=patient_tree.yview)

        for col in columns:
            patient_tree.heading(col, text=col)
            patient_tree.column(col, width=100)

        for patient in self.patient_record_data:
            patient_tree.insert("", tk.END, values=patient)

        # Billing Form
        form_frame = tk.Frame(billing_window, bg="#ffffff")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Consultation ($):", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        consultation_entry = tk.Entry(form_frame)
        consultation_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Medication ($):", bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        medication_entry = tk.Entry(form_frame)
        medication_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Room Charges ($):", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        room_entry = tk.Entry(form_frame)
        room_entry.grid(row=2, column=1, padx=5, pady=5)

        # Actions
        action_frame = tk.Frame(billing_window, bg="#ffffff")
        action_frame.pack(pady=15)

        tk.Button(action_frame, text="Calculate Bill", command=calculate_bill, bg="#27ae60", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Generate Report", command=self.open_patient_report_window, bg="#27ae60", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Back", command=self.start, bg="#3498db", fg="white", width=15).pack(side=tk.LEFT, padx=5)

    def open_patient_report_window(self):
        # Create a new window
        report_window = tk.Toplevel()
        report_window.title("Patient Reports")
        report_window.geometry("700x400")
        report_window.configure(bg="#ffffff")
        report_window.attributes('-fullscreen', True)

        tk.Label(report_window, text="Select Patient to Generate Report", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Treeview Frame
        tree_frame = tk.Frame(report_window)
        tree_frame.pack(pady=10, fill='both', expand=True)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Name", "Age", "Gender", "Contact", "Diagnosis")
        patient_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set, height=12)
        patient_tree.pack(fill='both', expand=True)

        tree_scroll.config(command=patient_tree.yview)

        # Define headings
        for col in columns:
            patient_tree.heading(col, text=col)
            patient_tree.column(col, width=100)

        # Insert patient data
        for patient in self.patient_record_data:
            patient_tree.insert("", tk.END, values=patient)

        # Text widget for report display
        report_text = tk.Text(report_window, height=10, bg="#f9f9f9", font=("Helvetica", 12))
        report_text.pack(padx=10, pady=10, fill='both', expand=True)

        def generate_report():
            selected = patient_tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a patient.")
                return
            item = patient_tree.item(selected)
            patient = item['values']

            room_info = "No room assigned"
            if hasattr(self, "room_bed_data"):
                for room in self.room_bed_data:
                    if len(patient) >= 7 and patient[6] == room[0]:
                        room_info = f"Room {room[0]} ({room[1]}), Status: {room[2]}"
                        break
                    elif room[3] == patient[1]:  # match by name
                        room_info = f"Room {room[0]} ({room[1]}), Status: {room[2]}"
                        break

            report = f"""
            === Patient Report ===

            Patient ID     : {patient[0]}
            Name           : {patient[1]}
            Age            : {patient[2]}
            Gender         : {patient[3]}
            Contact        : {patient[4]}
            Diagnosis      : {patient[5]}
            Assigned Room  : {room_info}
            """

            report_text.delete("1.0", tk.END)
            report_text.insert(tk.END, report.strip())

        # Buttons
        btn_frame = tk.Frame(report_window)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Generate Report", command=generate_report, bg="#9b59b6", fg="white", width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=report_window.destroy, bg="#e74c3c", fg="white", width=10).pack(side=tk.LEFT, padx=5)

    def report_generation(self):
        for window in tk._default_root.winfo_children():
            window.destroy()
        tk._default_root.destroy()

        report_window = tk.Tk()
        report_window.title("System Report")
        report_window.geometry("600x400")
        report_window.configure(bg="#ffffff")

        tk.Label(report_window, text="📊 System Report Summary", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Gather Data
        total_patients = len(self.patient_record_data)
        total_rooms = len(self.room_bed_data)
        occupied_rooms = sum(1 for r in self.room_bed_data if r[2] == "Occupied")
        available_rooms = total_rooms - occupied_rooms
        total_doctors = len(getattr(self, "doctor_schedule_data", [])) if hasattr(self, "doctor_schedule_data") else 0

        summary_text = (
            f"Total Patients: {total_patients}\n"
            f"Total Doctors: {total_doctors}\n"
            f"Total Rooms: {total_rooms}\n"
            f"Occupied Rooms: {occupied_rooms}\n"
            f"Available Rooms: {available_rooms}\n"
        )

        summary_label = tk.Label(report_window, text=summary_text, font=("Helvetica", 12), justify="left", bg="#ffffff")
        summary_label.pack(pady=10)

        def export_report():
            report = (
                "==== HOSPITAL SYSTEM REPORT ====\n"
                f"Total Patients     : {total_patients}\n"
                f"Total Doctors      : {total_doctors}\n"
                f"Total Rooms        : {total_rooms}\n"
                f" - Occupied        : {occupied_rooms}\n"
                f" - Available       : {available_rooms}\n"
                "\nGenerated by Hospital Management System"
            )
            with open("hospital_report.txt", "w") as f:
                f.write(report)
            messagebox.showinfo("Exported", "Report saved to 'hospital_report.txt'.")

        action_frame = tk.Frame(report_window, bg="#ffffff")
        action_frame.pack(pady=20)

        tk.Button(action_frame, text="Export Report", command=export_report, bg="#27ae60", fg="white", width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(action_frame, text="Back", command=self.start, bg="#3498db", fg="white", width=20).pack(side=tk.LEFT, padx=10)


    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            for window in tk._default_root.winfo_children():
                window.destroy()
            tk._default_root.destroy()


if __name__ == "__main__":
    app = HospitalManagementSystem()
    
