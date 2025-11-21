import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ My Task Manager")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        self.tasks = []

        # Color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#6366f1"
        self.secondary_color = "#ec4899"
        self.accent_color = "#8b5cf6"
        self.text_color = "#1f2937"
        self.white = "#ffffff"

        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="✨ My Tasks",
            font=("Arial", 32, "bold"),
            bg=self.primary_color,
            fg=self.white
        )
        title_label.pack(pady=15)

        subtitle_label = tk.Label(
            header_frame,
            text="Stay organized, stay productive",
            font=("Arial", 12),
            bg=self.primary_color,
            fg=self.white
        )
        subtitle_label.pack()

        # Main Container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Input Frame
        input_frame = tk.Frame(main_container, bg=self.white, relief=tk.FLAT)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # Task Entry
        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 14),
            relief=tk.FLAT,
            bg=self.white,
            fg=self.text_color,
            insertbackground=self.primary_color
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.task_entry.insert(0, "Add a new task...")
        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
        self.task_entry.bind("<FocusOut>", self.add_placeholder)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Add Button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add",
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg=self.white,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task,
            padx=20,
            pady=10
        )
        add_btn.pack(side=tk.RIGHT, padx=15, pady=10)

        # Button Frame
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        # Action Buttons
        buttons = [
            ("💾 Save Tasks", self.save_tasks, self.accent_color),
            ("📂 Load Tasks", self.load_tasks, self.secondary_color),
            ("🗑️ Clear All", self.clear_all_tasks, "#ef4444")
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 11, "bold"),
                bg=color,
                fg=self.white,
                relief=tk.FLAT,
                cursor="hand2",
                command=command,
                padx=15,
                pady=8
            )
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Task List Frame
        list_frame = tk.Frame(main_container, bg=self.white, relief=tk.FLAT)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Task Counter
        self.counter_label = tk.Label(
            list_frame,
            text="📝 0 tasks",
            font=("Arial", 11, "bold"),
            bg=self.white,
            fg=self.text_color,
            anchor=tk.W
        )
        self.counter_label.pack(fill=tk.X, padx=15, pady=(15, 10))

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))

        # Task Listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 12),
            bg=self.white,
            fg=self.text_color,
            selectbackground=self.primary_color,
            selectforeground=self.white,
            relief=tk.FLAT,
            activestyle="none",
            yscrollcommand=scrollbar.set,
            highlightthickness=0,
            borderwidth=0
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.config(command=self.task_listbox.yview)

        # Delete Button
        delete_btn = tk.Button(
            list_frame,
            text="🗑️ Delete Selected Task",
            font=("Arial", 11, "bold"),
            bg="#ef4444",
            fg=self.white,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.delete_task,
            pady=10
        )
        delete_btn.pack(fill=tk.X, padx=15, pady=(0, 15))

    def clear_placeholder(self, event):
        if self.task_entry.get() == "Add a new task...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg=self.text_color)

    def add_placeholder(self, event):
        if not self.task_entry.get():
            self.task_entry.insert(0, "Add a new task...")
            self.task_entry.config(fg="#9ca3af")

    def add_task(self):
        task = self.task_entry.get().strip()
        if task and task != "Add a new task...":
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, f"  ✓ {task}")
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, "Add a new task...")
            self.task_entry.config(fg="#9ca3af")
            self.update_counter()
            messagebox.showinfo("Success", "✅ Task added successfully!")
        else:
            messagebox.showwarning("Warning", "⚠️ Please enter a task!")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_index]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete this task?\n\n'{task}'"
            )

            if confirm:
                self.tasks.pop(selected_index)
                self.task_listbox.delete(selected_index)
                self.update_counter()
                messagebox.showinfo("Deleted", f"🗑️ Removed: '{task}'")
        except IndexError:
            messagebox.showwarning("Warning", "⚠️ Please select a task to delete!")

    def save_tasks(self):
        if not self.tasks:
            messagebox.showwarning("Warning", "⚠️ No tasks to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="tasks.txt"
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    for task in self.tasks:
                        f.write(task + "\n")
                messagebox.showinfo("Success", f"💾 {len(self.tasks)} task(s) saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tasks:\n{e}")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "r") as f:
                    loaded_tasks = [line.strip() for line in f if line.strip()]

                if loaded_tasks:
                    self.tasks = loaded_tasks
                    self.task_listbox.delete(0, tk.END)
                    for task in self.tasks:
                        self.task_listbox.insert(tk.END, f"  ✓ {task}")
                    self.update_counter()
                    messagebox.showinfo("Success", f"📂 Loaded {len(self.tasks)} task(s)!")
                else:
                    messagebox.showwarning("Warning", "⚠️ The file is empty!")
            except FileNotFoundError:
                messagebox.showerror("Error", "❌ File not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks:\n{e}")

    def clear_all_tasks(self):
        if not self.tasks:
            messagebox.showwarning("Warning", "⚠️ No tasks to clear!")
            return

        confirm = messagebox.askyesno(
            "Confirm Clear",
            f"Are you sure you want to delete all {len(self.tasks)} tasks?\n\nThis action cannot be undone!"
        )

        if confirm:
            self.tasks.clear()
            self.task_listbox.delete(0, tk.END)
            self.update_counter()
            messagebox.showinfo("Cleared", "🗑️ All tasks cleared!")

    def update_counter(self):
        count = len(self.tasks)
        self.counter_label.config(text=f"📝 {count} task{'s' if count != 1 else ''}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()