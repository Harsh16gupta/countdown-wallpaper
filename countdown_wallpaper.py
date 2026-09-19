#!/usr/bin/env python3
"""
90-Day Countdown Wallpaper System for Ubuntu GNOME.
Calculates remaining days from start date (Sept 1, 2026),
generates a minimalist pure black wallpaper, and applies it to GNOME.
"""

import argparse
import datetime
import os
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

START_DATE = datetime.date(2026, 9, 1)
START_DAYS = 90
BASE_DIR = Path.home() / ".local" / "share" / "countdown-wallpaper"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght].ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def calculate_days_left(target_date: datetime.date) -> int:
    """Calculate remaining days from target date."""
    elapsed = (target_date - START_DATE).days
    if elapsed < 0:
        return START_DAYS
    days_left = START_DAYS - elapsed
    return max(0, days_left)


def find_font(size: int):
    """Find and load the best available TrueType font."""
    for font_path in FONT_CANDIDATES:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_wallpaper(days_left: int, output_path: Path, width: int = 3840, height: int = 2160):
    """Render a clean, high-resolution minimal countdown wallpaper."""
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    num_font = find_font(440)
    num_str = str(days_left)

    # Measure number dimensions
    bbox_num = draw.textbbox((0, 0), num_str, font=num_font)
    w_num = bbox_num[2] - bbox_num[0]
    h_num = bbox_num[3] - bbox_num[1]

    center_x = width // 2
    center_y = height // 2

    # Center number both horizontally and vertically
    x_num = center_x - (w_num // 2) - bbox_num[0]
    y_num = center_y - (h_num // 2) - bbox_num[1]
    draw.text((x_num, y_num), num_str, fill=(255, 255, 255), font=num_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    return output_path


def apply_wallpaper(image_path: Path):
    """Set the wallpaper in GNOME for both light and dark modes."""
    uri = f"file://{image_path.resolve()}"
    cmd_base = ["gsettings", "set", "org.gnome.desktop.background"]

    subprocess.run(cmd_base + ["picture-uri", uri], check=True)
    subprocess.run(cmd_base + ["picture-uri-dark", uri], check=True)
    subprocess.run(cmd_base + ["picture-options", "zoom"], check=False)
    subprocess.run(cmd_base + ["primary-color", "#000000"], check=False)


def clean_old_wallpapers(current_file: Path):
    """Remove older wallpaper files in BASE_DIR to keep directory tidy."""
    for p in BASE_DIR.glob("wallpaper_*.png"):
        if p.resolve() != current_file.resolve():
            try:
                p.unlink()
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description="Update 90-day countdown wallpaper.")
    parser.add_argument(
        "--test-date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Simulate a specific date (YYYY-MM-DD) without updating the actual system wallpaper.",
    )
    parser.add_argument(
        "--test-days",
        type=int,
        help="Simulate a specific days-left count without updating the actual system wallpaper.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Explicit output path for the image.",
    )
    parser.add_argument(
        "--set",
        action="store_true",
        help="Force setting as wallpaper even when test options are specified.",
    )

    args = parser.parse_args()

    is_test = args.test_date is not None or args.test_days is not None
    should_set = (not is_test) or args.set

    if args.test_days is not None:
        days_left = max(0, min(START_DAYS, args.test_days))
        current_date = "TEST_DAYS"
    elif args.test_date is not None:
        days_left = calculate_days_left(args.test_date)
        current_date = args.test_date.isoformat()
    else:
        today = datetime.date.today()
        days_left = calculate_days_left(today)
        current_date = today.isoformat()

    if args.output:
        dest_path = args.output
    else:
        dest_path = BASE_DIR / f"wallpaper_{days_left}.png"

    render_wallpaper(days_left, dest_path)
    print(f"[{current_date}] Calculated {days_left} DAYS LEFT -> Generated {dest_path}")

    if should_set:
        apply_wallpaper(dest_path)
        clean_old_wallpapers(dest_path)
        print("Applied wallpaper to GNOME desktop background successfully.")


if __name__ == "__main__":
    main()
