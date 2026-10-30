# Dell S2725DS Input Switcher

A simple GUI tool to switch the input source on Dell S2725DS monitors using `ddcutil`.

## Features
- Switch between DisplayPort, HDMI 1, and HDMI 2
- Supports two monitors (identified by serial)
- Shows current input
- Optimized for CachyOS / Linux

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

Or run with sudo if preferred:
```bash
sudo python3 monitor_switch.py
```

## Notes
- On Windows, use Dell Display Manager instead.
- Input values are based on the S2725DS MCCS capabilities (0x0f = DP, 0x11 = HDMI 1, 0x12 = HDMI 2).
