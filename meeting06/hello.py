import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Great To-Do App")
        self.root.geometry("400x500")
        
        # Theme State
        self.dark_mode = False
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.colors = {
            'light': {'bg': '#ffffff', 'fg': '#333333', 'entry_bg': '#f0f0f0', 'list_bg': '#ffffff', 'sel_bg': '#0078d7'},
            'dark': {'bg': '#2d2d2d', 'fg': '#ffffff', 'entry_bg': '#404040', 'list_bg': '#333333', 'sel_bg': '#555555'}
        }
        
        # Main Frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = ttk.Label(self.header_frame, text="My Tasks", font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        self.theme_btn = ttk.Button(self.header_frame, text="🌙", width=3, command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Inupt Area
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.input_frame, textvariable=self.task_var, font=("Segoe UI", 10))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        self.add_btn = ttk.Button(self.input_frame, text="Add", command=self.add_task)
        self.add_btn.pack(side=tk.RIGHT)
        
        # List Area
        self.list_frame = ttk.Frame(self.main_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_list = tk.Listbox(
            self.list_frame, 
            font=("Segoe UI", 11), 
            bd=0, 
            highlightthickness=0,
            activestyle='none',
            selectmode=tk.EXTENDED,
            yscrollcommand=self.scrollbar.set
        )
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.task_list.yview)
        
        # Bottom Controls
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        self.delete_btn = ttk.Button(self.controls_frame, text="Delete Selected", command=self.delete_task)
        self.delete_btn.pack(side=tk.RIGHT)
        
        self.apply_theme()
        self.load_tasks()

    def apply_theme(self):
        theme = 'dark' if self.dark_mode else 'light'
        c = self.colors[theme]
        
        self.root.configure(bg=c['bg'])
        self.style.configure('TFrame', background=c['bg'])
        self.style.configure('TLabel', background=c['bg'], foreground=c['fg'])
        self.style.configure('TButton', font=('Segoe UI', 9))
        
        self.task_list.configure(bg=c['list_bg'], fg=c['fg'], selectbackground=c['sel_bg'])
        
        # Update button icon
        self.theme_btn.configure(text="☀️" if self.dark_mode else "🌙")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.task_list.insert(tk.END, task)
            self.task_var.set("")
            self.save_tasks()

    def delete_task(self):
        selection = self.task_list.curselection()
        if not selection:
            return
        
        for index in reversed(selection):
            self.task_list.delete(index)
        self.save_tasks()

    def save_tasks(self):
        tasks = self.task_list.get(0, tk.END)
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(list(tasks), f)
        except Exception as e:
            pass # Fail silently for a simple app

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    tasks = json.load(f)
                    for task in tasks:
                        self.task_list.insert(tk.END, task)
            except Exception:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
