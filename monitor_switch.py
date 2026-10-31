#!/usr/bin/env python3
"""
Dell S2725DS Input Switcher

Pick the monitors and the input, then click Apply.
Nothing talks to sudo until Apply. Canceling the password box does not
count as a failed login.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

INPUTS = {
    "DisplayPort": "0x0f",
    "HDMI 1": "0x11",
    "HDMI 2": "0x12",
}

MONITORS = [
    ("Display 1 (6WX7614)", (1,)),
    ("Display 2 (5GF6614)", (2,)),
    ("Both monitors", (1, 2)),
]

def is_linux():
    return sys.platform.startswith("linux")

def ask_password(parent):
    """Return the password, or None if the user cancels. Does not call sudo."""
    dialog = tk.Toplevel(parent)
    dialog.title("sudo password")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    tk.Label(
        dialog,
        text="Enter your sudo password to apply the change.",
        padx=12,
        pady=8,
    ).pack()

    entry = tk.Entry(dialog, show="*", width=32)
    entry.pack(padx=12, pady=(0, 8))
    entry.focus_set()

    result = {"password": None}

    def accept(_event=None):
        result["password"] = entry.get()
        dialog.destroy()

    def cancel(_event=None):
        dialog.destroy()

    buttons = tk.Frame(dialog)
    buttons.pack(pady=(0, 10))
    tk.Button(buttons, text="Apply", width=10, command=accept).pack(side="left", padx=6)
    tk.Button(buttons, text="Cancel", width=10, command=cancel).pack(side="left", padx=6)

    dialog.bind("<Return>", accept)
    dialog.bind("<Escape>", cancel)
    dialog.protocol("WM_DELETE_WINDOW", cancel)

    parent.wait_window(dialog)
    return result["password"]

def sudo_ddcutil(password, displays, value):
    """One sudo invocation for every selected display."""
    parts = [
        f"ddcutil --display {display} setvcp 60 {value}"
        for display in displays
    ]
    script = " && ".join(parts)
    try:
        result = subprocess.run(
            ["sudo", "-S", "-p", "", "sh", "-c", script],
            input=password + "\n",
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as exc:
        return False, str(exc)
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output.strip()

class MonitorSwitcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor Input Switcher")
        self.geometry("420x360")
        self.resizable(False, False)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "monitor_switch.png")
        if os.path.exists(icon_path):
            try:
                img = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, img)
                self._icon = img
            except Exception:
                pass

        tk.Label(self, text="Dell S2725DS Input Switcher", font=("Arial", 14, "bold")).pack(pady=(12, 8))

        if not is_linux():
            tk.Label(
                self,
                text="Running on Windows.\nUse Dell Display Manager for full control.\n\nThis tool is for CachyOS.",
                fg="blue",
                justify="center",
            ).pack(pady=20)
            tk.Button(self, text="Close", command=self.destroy, width=15).pack(pady=20)
            return

        body = tk.Frame(self)
        body.pack(padx=16, fill="x")

        left = tk.Frame(body)
        left.pack(side="left", padx=(0, 16))
        tk.Label(left, text="Monitors").pack(anchor="w")
        self.monitor_list = tk.Listbox(left, height=3, width=24, exportselection=False)
        for label, _displays in MONITORS:
            self.monitor_list.insert(tk.END, label)
        self.monitor_list.selection_set(0)
        self.monitor_list.pack()

        right = tk.Frame(body)
        right.pack(side="left")
        tk.Label(right, text="Input").pack(anchor="w")
        self.input_list = tk.Listbox(right, height=3, width=18, exportselection=False)
        for name in INPUTS:
            self.input_list.insert(tk.END, name)
        self.input_list.selection_set(0)
        self.input_list.pack()

        self.status = tk.Label(
            self,
            text="sudo runs only when you click Apply.",
            fg="gray",
            wraplength=380,
            justify="center",
        )
        self.status.pack(pady=16)

        tk.Button(self, text="Apply", width=16, command=self.on_apply).pack()

    def selected_monitors(self):
        picked = self.monitor_list.curselection()
        if not picked:
            return None
        return MONITORS[picked[0]]

    def selected_input(self):
        picked = self.input_list.curselection()
        if not picked:
            return None
        name = self.input_list.get(picked[0])
        return name, INPUTS[name]

    def on_apply(self):
        monitors = self.selected_monitors()
        chosen = self.selected_input()
        if monitors is None or chosen is None:
            messagebox.showerror("Nothing selected", "Select a monitor and an input first.")
            return

        label, displays = monitors
        input_name, value = chosen

        password = ask_password(self)
        if not password:
            self.status.config(text="Canceled. Nothing was sent.")
            return

        try:
            ok, output = sudo_ddcutil(password, displays, value)
        finally:
            password = None

        if ok:
            self.status.config(text=f"{label} set to {input_name}.")
            messagebox.showinfo("Applied", f"{label} switched to {input_name}.")
        else:
            self.status.config(text="Apply failed.")
            messagebox.showerror("Error", output or "sudo or ddcutil failed.")

if __name__ == "__main__":
    if is_linux():
        try:
            subprocess.run(["ddcutil", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ddcutil not found. Install with: sudo pacman -S ddcutil")
            sys.exit(1)

    app = MonitorSwitcher()
    app.mainloop()
