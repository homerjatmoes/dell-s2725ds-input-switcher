# Dell S2725DS Input Switcher

A simple GUI tool to switch the input source on Dell S2725DS monitors using `ddcutil`.

## Features
- Pick monitors and an input from lists
- Apply button asks for the sudo password only after the choice is made
- Canceling the password box does not call sudo and does not count as a failed login
- Supports one monitor or both at once
- Optimized for CachyOS / Linux
- Optional application menu entry and window icon

## Requirements
- Linux (CachyOS recommended)
- `ddcutil` installed (`sudo pacman -S ddcutil`)
- DDC/CI enabled in the monitor OSD
- Python 3 with tkinter (usually pre-installed)

## Usage
```bash
chmod +x monitor_switch.py
python3 monitor_switch.py
```

Select the monitors and the input, then click Apply. The password box appears only then.

## Application menu / icon
1. Place `monitor_switch.png` (the icon) in the same directory as the script.
2. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
3. The entry will appear in your application menu. You may need to log out/in or run:
   ```bash
   update-desktop-database ~/.local/share/applications
   ```

The script also uses the PNG as the window icon when it is present next to the script.

## Notes
- On Windows, use Dell Display Manager instead.
- Input values are based on the S2725DS MCCS capabilities (0x0f = DP, 0x11 = HDMI 1, 0x12 = HDMI 2).
