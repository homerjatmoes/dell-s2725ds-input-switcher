#!/bin/bash
# Install Monitor Input Switcher to the application menu

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/monitor-switcher.desktop"
ICON_SRC="$SCRIPT_DIR/monitor_switch.png"
ICON_DEST="$HOME/.local/share/icons/monitor-switcher.png"
DESKTOP_DEST="$HOME/.local/share/applications/monitor-switcher.desktop"

# Update the Exec path in the desktop file to the actual location
sed "s|%h/dell-s2725ds-input-switcher|$SCRIPT_DIR|g" "$DESKTOP_FILE" > /tmp/monitor-switcher.desktop.tmp

mkdir -p "$HOME/.local/share/icons"
mkdir -p "$HOME/.local/share/applications"

if [ -f "$ICON_SRC" ]; then
    cp "$ICON_SRC" "$ICON_DEST"
    echo "Icon installed to $ICON_DEST"
else
    echo "Warning: monitor_switch.png not found in $SCRIPT_DIR"
    echo "Place the icon file there and re-run, or set the Icon path manually."
fi

cp /tmp/monitor-switcher.desktop.tmp "$DESKTOP_DEST"
chmod +x "$DESKTOP_DEST"

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

echo "Installed to application menu."
echo "You may need to log out and back in, or run: update-desktop-database ~/.local/share/applications"
