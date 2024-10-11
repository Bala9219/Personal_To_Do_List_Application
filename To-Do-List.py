import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

class ModernTodo:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("700x700")
        self.master.configure(bg="#00B2E2")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Tframe", background="#00B2E2")
        style.configure("TButton", padding=14, font=('Helvetica', 14), background="#0097C8", foreground="white")
        style.configure("TEntry", padding=14, font=('Helvetica', 14), foreground="black")
        style.configure("Treeview", background="white", foreground="black")
        style.configure("Treeview.Heading", font=('Helvetica', 15, 'bold'), background="#0097C8", foreground="white")

        self.frame = ttk.Frame(self.master, padding="14", relief=tk.SUNKEN)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=30)
        self.task_entry.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.frame, textvariable=self.category_var, values=["Work", "Personal", "Urgent"])
        self.category_dropdown.grid(row=0, column=1, padx=5, pady=10)
        self.category_dropdown.set("Select Category")

        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        self.edit_button = ttk.Button(self.frame, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=1, column=1, padx=5, pady=10)

        self.task_tree = ttk.Treeview(self.frame, columns=("Task", "Category"), show="headings", height=15)
        self.task_tree.heading("Task", text="Tasks")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=3, column=2, sticky="ns")
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        self.delete_button = ttk.Button(self.frame, text="Delete Tasks", command=self.delete_task)
        self.delete_button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.complete_button = ttk.Button(self.frame, text="Complete Task", command=self.complete_task)
        self.complete_button.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        self.save_button = ttk.Button(self.frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.load_tasks()

    def add_task(self):
        task = self.task_var.get()
        category = self.category_var.get()
        if task and category:
            if any(task == self.task_tree.item(child)['values'][0] for child in self.task_tree.get_children()):
                messagebox.showwarning("Warning", "Task already exists.")
            else:
                self.task_tree.insert("", tk.END, values=(task, category))
                self.task_var.set("")
                self.category_var.set("Select Category")
                messagebox.showinfo("Success", "Task added successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a task and select a category.")

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            new_task = self.task_var.get()
            category = self.category_var.get()
            if new_task and category:
                if any(new_task == self.task_tree.item(child)['values'][0] for child in self.task_tree.get_children()):
                    messagebox.showwarning("Warning", "Task already exists.")
                else:
                    self.task_tree.item(selected_item, values=(new_task, category))
                    self.task_var.set("")
                    self.category_var.set("Select Category")
                    messagebox.showinfo("Success", "Task updated successfully!")
            else:
                messagebox.showwarning("Warning", "Please enter a new task and select a category.")
        else:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def complete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task = self.task_tree.item(selected_item)['values'][0]
            category = self.task_tree.item(selected_item)['values'][1]
            completed_task = f"{task} [Completed]"
            self.task_tree.item(selected_item, values=(completed_task, category))
            self.task_tree.item(selected_item, tags=('completed',))
            self.task_tree.tag_configure('completed', foreground='gray')
            messagebox.showinfo("Success", "Task marked as complete!")
        else:
            messagebox.showwarning("Warning", "Please select a task to complete.")

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            self.task_tree.delete(selected_item)
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def save_tasks(self):
        tasks = [(self.task_tree.item(child)['values'][0], 
                   self.task_tree.item(child)['values'][1]) for child in self.task_tree.get_children()]
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
            for task, category in tasks:
                self.task_tree.insert('', tk.END, values=(task, category))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTodo(root)
    root.mainloop()
