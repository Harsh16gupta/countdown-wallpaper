#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_BIN_DIR="$HOME/.local/share/countdown-wallpaper"
TARGET_SYSTEMD_DIR="$HOME/.config/systemd/user"

echo "==> Creating directories..."
mkdir -p "$TARGET_BIN_DIR" "$TARGET_SYSTEMD_DIR"

echo "==> Installing countdown script..."
cp "$SCRIPT_DIR/countdown_wallpaper.py" "$TARGET_BIN_DIR/countdown_wallpaper.py"
chmod +x "$TARGET_BIN_DIR/countdown_wallpaper.py"

echo "==> Installing systemd user units..."
cp "$SCRIPT_DIR/systemd/countdown-wallpaper.service" "$TARGET_SYSTEMD_DIR/"
cp "$SCRIPT_DIR/systemd/countdown-wallpaper.timer" "$TARGET_SYSTEMD_DIR/"

echo "==> Reloading systemd user daemon and enabling timer..."
systemctl --user daemon-reload
systemctl --user enable --now countdown-wallpaper.timer

echo "==> Generating and applying wallpaper now..."
systemctl --user start countdown-wallpaper.service

echo "==> Setup complete! Your countdown wallpaper is active."
