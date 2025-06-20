import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# === Constants ===
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'labeled_log.csv'))

# === Helper Functions ===
def load_sessions():
    sessions = []
    if not os.path.exists(CSV_PATH):
        return sessions
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Group as 'Meal' or 'Work'
            label = 'Meal' if row.get('Category', '').lower() == 'meal' else 'Work'
            sessions.append({
                'Start Time': row['Start Time'],
                'End Time': row['End Time'],
                'Duration': row['Duration'],
                'Type': label,
                'Row': row
            })
    return sessions

def save_sessions(sessions):
    if not sessions:
        return
    fieldnames = list(sessions[0]['Row'].keys())
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in sessions:
            writer.writerow(s['Row'])

# === GUI ===
class TimesheetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Employee Timesheet')
        self.configure(bg='white')
        self.geometry('700x500')
        self.resizable(False, False)
        self.sessions = load_sessions()
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text='Employee Timesheet', font=('Helvetica Neue', 22, 'bold'), fg='#ec1c24', bg='white')
        title.pack(pady=(20, 10))
        self.tree = ttk.Treeview(self, columns=('Type', 'Start', 'End', 'Duration'), show='headings', height=15)
        self.tree.heading('Type', text='Type')
        self.tree.heading('Start', text='Start Time')
        self.tree.heading('End', text='End Time')
        self.tree.heading('Duration', text='Duration')
        self.tree.column('Type', width=80, anchor='center')
        self.tree.column('Start', width=180, anchor='center')
        self.tree.column('End', width=180, anchor='center')
        self.tree.column('Duration', width=120, anchor='center')
        self.tree.pack(padx=20, pady=10, fill='x')
        self.populate_tree()
        edit_btn = tk.Button(self, text='Edit Selected', command=self.edit_selected, bg='#ec1c24', fg='white', font=('Helvetica Neue', 12, 'bold'), relief='flat', padx=16, pady=6)
        edit_btn.pack(pady=10)

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, s in enumerate(self.sessions):
            self.tree.insert('', 'end', iid=idx, values=(s['Type'], s['Start Time'], s['End Time'], s['Duration']))

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('No selection', 'Please select a session to edit.')
            return
        idx = int(selected[0])
        session = self.sessions[idx]
        EditDialog(self, session, self.on_edit_done, idx)

    def on_edit_done(self, idx, new_start, new_end):
        # Update session
        self.sessions[idx]['Start Time'] = new_start
        self.sessions[idx]['End Time'] = new_end
        self.sessions[idx]['Row']['Start Time'] = new_start
        self.sessions[idx]['Row']['End Time'] = new_end
        # Recalculate duration
        try:
            dt1 = datetime.strptime(new_start, '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime(new_end, '%Y-%m-%d %H:%M:%S')
            duration = str(dt2 - dt1).split('.')[0]
        except Exception:
            duration = ''
        self.sessions[idx]['Duration'] = duration
        self.sessions[idx]['Row']['Duration'] = duration
        save_sessions(self.sessions)
        self.populate_tree()

class EditDialog(tk.Toplevel):
    def __init__(self, parent, session, callback, idx):
        super().__init__(parent)
        self.title('Edit Session')
        self.configure(bg='white')
        self.geometry('350x200')
        self.resizable(False, False)
        self.callback = callback
        self.idx = idx
        tk.Label(self, text='Edit Start Time:', bg='white').pack(pady=(20, 2))
        self.start_var = tk.StringVar(value=session['Start Time'])
        tk.Entry(self, textvariable=self.start_var, width=30).pack()
        tk.Label(self, text='Edit End Time:', bg='white').pack(pady=(10, 2))
        self.end_var = tk.StringVar(value=session['End Time'])
        tk.Entry(self, textvariable=self.end_var, width=30).pack()
        tk.Button(self, text='Save', command=self.save, bg='#ec1c24', fg='white', font=('Helvetica Neue', 11, 'bold'), relief='flat', padx=12, pady=4).pack(pady=18)
    def save(self):
        self.callback(self.idx, self.start_var.get(), self.end_var.get())
        self.destroy()

if __name__ == '__main__':
    app = TimesheetApp()
    app.mainloop()
