# 90-Day Countdown Wallpaper for Ubuntu Linux

A minimalist, pure black (`#000000`) 4K wallpaper for Ubuntu GNOME that counts down 90 days.

## Features

- **Minimalist Aesthetic**: Solid black background with high-contrast, clean typography (`Ubuntu Bold`) and tracked subtitles.
- **Set & Forget**: Runs via `systemd --user` timer every midnight (`00:00:05`).
- **Sleep & Power Catch-up**: Uses `Persistent=true` and hourly checks so that if your laptop is suspended, asleep, or powered off over midnight, it immediately recalculates the correct date upon waking up.
- **Dual Display Ready**: Crisp 3840×2160 resolution that scales seamlessly across all aspect ratios (16:9, 16:10).

## Quick Start

### 1. Requirements
- Ubuntu 22.04+ (GNOME desktop environment)
- Python 3 with Pillow:
  ```bash
  sudo apt install python3-pil
  ```

### 2. Installation
Clone the repository and run:
```bash
./install.sh
```

### 3. Check Status
Check the timer status at any time:
```bash
systemctl --user list-timers countdown-wallpaper.timer
```

To run manually or test a future date:
```bash
python3 countdown_wallpaper.py --test-date 2026-09-10
```

## How It Works

- The challenge starts on **September 1, 2026** (Day 90).
- Calculates days left using calendar arithmetic:
  $$\text{Days Left} = \max(0, 90 - (\text{today} - \text{2026-09-01}).\text{days})$$
- Automatically updates GNOME's `picture-uri` and `picture-uri-dark`.
- Counts down to `0 DAYS LEFT`.
