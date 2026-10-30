#!/usr/bin/env python3
"""
Dell S2725DS Input Switcher
Simple GUI for switching monitor inputs via ddcutil (Linux) or a note for Windows.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Input source values from your ddcutil capabilities
INPUTS = {
    "DisplayPort": "0x0f",
    "HDMI 1": "0x11",
    "HDMI 2": "0x12",
}

def is_linux():
    return sys.platform.startswith("linux")

def run_ddcutil(args, display=None):
    cmd = ["sudo", "ddcutil"] + args
    if display is not None:
        cmd.extend(["--display", str(display)])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def switch_input(input_name, display_num):
    if not is_linux():
        messagebox.showinfo(
            "Windows",
            "This script is designed for CachyOS/Linux with ddcutil.\n"
            "On Windows, use Dell Display Manager or switch inputs manually on the monitor."
        )
        return

    value = INPUTS.get(input_name)
    if not value:
        messagebox.showerror("Error", f"Unknown input: {input_name}")
        return

    success, output = run_ddcutil(["setvcp", "60", value], display_num)
    if success:
        messagebox.showinfo("Success", f"Switched Display {display_num} to {input_name}")
    else:
        messagebox.showerror("Error", f"Failed to switch:\n{output}")

def get_current_input(display_num):
    if not is_linux():
        return "N/A (Windows)"
    success, output = run_ddcutil(["getvcp", "60"], display_num)
    if success:
        # Parse the current value from output
        for line in output.splitlines():
            if "Input Source" in line or "sl=" in line:
                return line.strip()
        return output.strip() or "Unknown"
    return "Error reading"

class MonitorSwitcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor Input Switcher")
        self.geometry("420x320")
        self.resizable(False, False)

        # Title
        tk.Label(self, text="Dell S2725DS Input Switcher", font=("Arial", 14, "bold")).pack(pady=10)

        if not is_linux():
            tk.Label(
                self,
                text="Running on Windows.\nUse Dell Display Manager for full control.\n\n"
                     "This tool is optimized for CachyOS.",
                fg="blue",
                justify="center"
            ).pack(pady=20)
            tk.Button(self, text="Close", command=self.destroy, width=15).pack(pady=20)
            return

        # Display selection
        tk.Label(self, text="Select Display:").pack()
        self.display_var = tk.IntVar(value=1)
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Radiobutton(frame, text="Display 1 (6WX7614)", variable=self.display_var, value=1).pack(side="left", padx=10)
        tk.Radiobutton(frame, text="Display 2 (5GF6614)", variable=self.display_var, value=2).pack(side="left", padx=10)

        # Current input
        self.current_label = tk.Label(self, text="Current: checking...", fg="gray")
        self.current_label.pack(pady=5)
        self.update_current()

        # Buttons
        tk.Label(self, text="Switch to:").pack(pady=(10, 5))
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        for name in INPUTS.keys():
            tk.Button(
                btn_frame,
                text=name,
                width=12,
                command=lambda n=name: self.on_switch(n)
            ).pack(side="left", padx=5)

        # Refresh button
        tk.Button(self, text="Refresh Current", command=self.update_current).pack(pady=15)

    def update_current(self):
        disp = self.display_var.get()
        current = get_current_input(disp)
        self.current_label.config(text=f"Display {disp} current: {current}")

    def on_switch(self, input_name):
        disp = self.display_var.get()
        switch_input(input_name, disp)
        self.after(500, self.update_current)  # refresh after switch

if __name__ == "__main__":
    # Check if ddcutil is available on Linux
    if is_linux():
        try:
            subprocess.run(["ddcutil", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ddcutil not found. Install with: sudo pacman -S ddcutil")
            sys.exit(1)

    app = MonitorSwitcher()
    app.mainloop()
