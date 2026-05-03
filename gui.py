import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

from enroll import enroll_face
from recognize import start_recognition


def enroll():

    name = name_entry.get()

    if name.strip() == "":
        status_label.config(text="Enter a valid name")
        return

    enroll_face(name)

    status_label.config(
        text=f"{name} enrolled successfully"
    )


def recognize():

    status_label.config(
        text="Starting recognition..."
    )

    start_recognition()


def view_attendance():

    if not os.path.exists("attendance.csv"):

        status_label.config(
            text="No attendance file found"
        )

        return

    window = tk.Toplevel(root)

    window.title("Attendance Records")

    tree = ttk.Treeview(
        window,
        columns=("Name", "Time", "Date"),
        show="headings"
    )

    tree.heading("Name", text="Name")
    tree.heading("Time", text="Time")
    tree.heading("Date", text="Date")

    tree.pack(fill="both", expand=True)

    df = pd.read_csv("attendance.csv")

    for _, row in df.iterrows():

        tree.insert(
            "",
            "end",
            values=(
                row["Name"],
                row["Time"],
                row["Date"]
            )
        )


root = tk.Tk()

root.title("Face Attendance System")

root.geometry("350x300")

title_label = tk.Label(
    root,
    text="Face Attendance System",
    font=("Arial", 14, "bold")
)

title_label.pack(pady=10)

name_label = tk.Label(
    root,
    text="Enter Name"
)

name_label.pack()

name_entry = tk.Entry(root)

name_entry.pack(pady=5)

enroll_button = tk.Button(
    root,
    text="Enroll Face",
    width=20,
    command=enroll
)

enroll_button.pack(pady=5)

recognize_button = tk.Button(
    root,
    text="Start Attendance",
    width=20,
    command=recognize
)

recognize_button.pack(pady=5)

view_button = tk.Button(
    root,
    text="View Attendance",
    width=20,
    command=view_attendance
)

view_button.pack(pady=5)

exit_button = tk.Button(
    root,
    text="Exit",
    width=20,
    command=root.destroy
)

exit_button.pack(pady=5)

status_label = tk.Label(
    root,
    text="System Ready",
    fg="blue"
)

status_label.pack(pady=10)

root.mainloop()