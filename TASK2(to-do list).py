import tkinter as tk
from tkinter import messagebox
import os

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("400x400")

        self.tasks = []

        self.task_entry = tk.Entry(root, width=40, font=("Arial", 14))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(root, text="Add Task", command=self.add_task, font=("Arial", 12), bg="#4CAF50", fg="white")
        add_button.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        tk.Label(root, text="Tasks", font=("Arial", 14, "bold")).grid(row=1, column=0, columnspan=2)

        self.task_listbox = tk.Listbox(root, width=50, height=12, font=("Arial", 12))
        self.task_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        complete_button = tk.Button(root, text="Mark Complete", command=self.mark_complete, font=("Arial", 12), bg="#2196F3", fg="white")
        complete_button.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, font=("Arial", 12), bg="#f44336", fg="white")
        delete_button.grid(row=3, column=1, padx=10, pady=10, sticky="W")

        clear_button = tk.Button(root, text="Clear All", command=self.clear_tasks, font=("Arial", 12), bg="#FFC107", fg="white")
        clear_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.load_tasks()

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()  
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index] = f"{self.tasks[selected_index]} (Completed)"
            self.update_task_listbox()
            self.save_tasks()  
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as complete.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
            self.save_tasks()  
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def clear_tasks(self):
        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?")
        if confirmed:
            self.tasks = []
            self.update_task_listbox()
            self.save_tasks()  

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task in self.tasks:
                f.write(task + "\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as f:
                self.tasks = [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()