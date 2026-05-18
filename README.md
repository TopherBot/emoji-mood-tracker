# Emoji Mood Tracker

A **tiny** command‑line tool to log your mood with a single emoji.

## Why?
- Instant tiny‑project scaffolding – just drop the script and start logging.
- Quick‑turn emoji‑based utility – perfect for a one‑liner mood update.
- Optional Telegram launch alert to keep you notified.

## Features
- Log a mood emoji with an optional note.
- Stores entries in `mood_log.json` in the same directory.
- `--summary` flag shows a quick count of each mood.
- `--notify` flag sends a Telegram message (requires a bot token & chat ID).

## Installation
```bash
# Requires Python 3.8+
git clone https://github.com/yourname/emoji-mood-tracker.git
cd emoji-mood-tracker
pip install -r requirements.txt   # optional, only if you use --notify
```

## Usage
```bash
# Log a mood (emoji must be a single Unicode emoji)
python main.py 😀 "Feeling great!"

# Show a summary of logged moods
python main.py --summary

# Send a Telegram alert (use environment variables for security)
export TG_BOT_TOKEN=YOUR_BOT_TOKEN
export TG_CHAT_ID=YOUR_CHAT_ID
python main.py 🎉 "Launch day!" --notify
```

## License
MIT – see LICENSE file.
