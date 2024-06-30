import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("800x600")
        self.root.config(bg="#e6e6e6")

        self.conn = sqlite3.connect('contacts.db')
        self.c = self.conn.cursor()
        self.create_table()

        self.create_gui()

    def create_table(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL,
                             phone TEXT NOT NULL,
                             email TEXT,
                             address TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def create_gui(self):
        self.top_frame = tk.Frame(self.root, bg="#e6e6e6", pady=10)
        self.top_frame.pack(fill=tk.X)

        self.middle_frame = tk.Frame(self.root, bg="#e6e6e6", pady=10)
        self.middle_frame.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.root, bg="#e6e6e6", pady=10)
        self.bottom_frame.pack(fill=tk.X)

        self.create_label_entry("Name:", 0)
        self.create_label_entry("Phone:", 1)
        self.create_label_entry("Email:", 2)
        self.create_label_entry("Address:", 3)

        self.create_buttons()

        self.contacts_tree = ttk.Treeview(self.middle_frame, columns=("Name", "Phone", "Email", "Address"), show="headings", height=15)
        self.contacts_tree.heading("Name", text="Name")
        self.contacts_tree.heading("Phone", text="Phone")
        self.contacts_tree.heading("Email", text="Email")
        self.contacts_tree.heading("Address", text="Address")
        self.contacts_tree.column("Name", width=150)
        self.contacts_tree.column("Phone", width=100)
        self.contacts_tree.column("Email", width=150)
        self.contacts_tree.column("Address", width=150)

        self.scrollbar = ttk.Scrollbar(self.middle_frame, orient="vertical", command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscroll=self.scrollbar.set)

        self.contacts_tree.bind('<<TreeviewSelect>>', self.on_contact_select)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.bottom_frame, textvariable=self.search_var, width=50, font=("Helvetica", 12))
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_button = tk.Button(self.bottom_frame, text="Search", command=self.search_contact, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.search_button.pack(side=tk.LEFT, padx=10)
        self.reset_button = tk.Button(self.bottom_frame, text="Reset", command=self.view_contacts, bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def create_label_entry(self, text, row):
        label = tk.Label(self.top_frame, text=text, bg="#e6e6e6", font=("Helvetica", 12))
        label.grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(self.top_frame, width=30, font=("Helvetica", 10))
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"{text[:-1].lower()}_entry", entry)

    def create_buttons(self):
        buttons_frame = tk.Frame(self.top_frame, bg="#e6e6e6")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)
        self.create_button(buttons_frame, "Add Contact", self.add_contact, "#4CAF50")
        self.create_button(buttons_frame, "Update Contact", self.update_contact, "#FF9800")
        self.create_button(buttons_frame, "Delete Contact", self.delete_contact, "#f44336")
        self.create_button(buttons_frame, "View Contacts", self.view_contacts, "#2196F3")

    def create_button(self, frame, text, command, color):
        button = tk.Button(frame, text=text, command=command, width=15, bg=color, fg="white", font=("Helvetica", 10, "bold"))
        button.pack(side=tk.LEFT, padx=5)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            try:
                self.c.execute('''INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)''', (name, phone, email, address))
                self.conn.commit()
                messagebox.showinfo("Success", "Contact added successfully!")
                self.clear_entries()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter at least Name and Phone number.")

    def view_contacts(self):
        self.contacts_tree.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side="right", fill="y")
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        try:
            self.c.execute('''SELECT name, phone, email, address FROM contacts''')
            contacts = self.c.fetchall()
            for contact in contacts:
                self.contacts_tree.insert('', tk.END, values=contact)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def on_contact_select(self, event):
        selected_item = self.contacts_tree.selection()
        if selected_item:
            contact = self.contacts_tree.item(selected_item[0], 'values')
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, contact[0])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(tk.END, contact[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(tk.END, contact[2])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(tk.END, contact[3])

    def update_contact(self):
        selected_item = self.contacts_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact from the list.")
            return

        old_contact = self.contacts_tree.item(selected_item[0], 'values')
        old_name, old_phone = old_contact[0], old_contact[1]
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            try:
                self.c.execute('''UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE name=? AND phone=?''',
                               (name, phone, email, address, old_name, old_phone))
                self.conn.commit()
                messagebox.showinfo("Success", "Contact updated successfully!")
                self.clear_entries()
                self.view_contacts()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter at least Name and Phone number.")

    def delete_contact(self):
        selected_item = self.contacts_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact from the list.")
            return

        contact = self.contacts_tree.item(selected_item[0], 'values')
        name, phone = contact[0], contact[1]

        try:
            self.c.execute('''DELETE FROM contacts WHERE name=? AND phone=?''', (name, phone))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.clear_entries()
            self.view_contacts()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def search_contact(self):
        search_text = self.search_var.get().lower()
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        try:
            self.c.execute('''SELECT name, phone, email, address FROM contacts''')
            contacts = self.c.fetchall()
            for contact in contacts:
                if search_text in contact[0].lower() or search_text in contact[1]:
                    self.contacts_tree.insert('', tk.END, values=contact)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
