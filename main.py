#!/usr/bin/env python3
"""emoji-mood-tracker: Tiny CLI mood logger.

Usage:
  python main.py <emoji> [note]          # Log a mood
  python main.py --summary                # Show summary
  python main.py <emoji> [note] --notify  # Log + Telegram alert

Environment variables for Telegram (optional):
  TG_BOT_TOKEN - Bot token from BotFather
  TG_CHAT_ID   - Chat ID to send the message to
"""
import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime

LOG_FILE = "mood_log.json"

def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_log(entry):
    data = load_log()
    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_mood(emoji, note, notify):
    if len(emoji.strip()) != 1:
        print("Error: Emoji must be a single Unicode character.")
        sys.exit(1)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "emoji": emoji,
        "note": note or "",
    }
    save_log(entry)
    print(f"Logged mood: {emoji} {note or ''}")
    if notify:
        send_telegram(entry)

def show_summary():
    data = load_log()
    if not data:
        print("No mood entries found.")
        return
    counts = Counter(e["emoji"] for e in data)
    print("Mood summary:")
    for emoji, cnt in counts.most_common():
        print(f"  {emoji}: {cnt}")

def send_telegram(entry):
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    if not token or not chat_id:
        print("Telegram env vars not set; skipping notification.")
        return
    try:
        import requests
    except ImportError:
        print("requests library missing; install it to use Telegram notifications.")
        return
    text = f"Mood logged: {entry['emoji']}\nNote: {entry['note']}\nTime: {entry['timestamp']}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    resp = requests.post(url, data=payload)
    if resp.ok:
        print("Telegram notification sent.")
    else:
        print("Failed to send Telegram message:", resp.text)

def main():
    parser = argparse.ArgumentParser(description="Tiny emoji mood tracker")
    parser.add_argument("emoji", nargs="?", help="Mood emoji (single character)")
    parser.add_argument("note", nargs="*", help="Optional free‑text note")
    parser.add_argument("--summary", action="store_true", help="Show mood summary")
    parser.add_argument("--notify", action="store_true", help="Send Telegram notification")
    args = parser.parse_args()

    if args.summary:
        show_summary()
        return

    if not args.emoji:
        parser.print_help()
        sys.exit(1)

    note_text = " ".join(args.note).strip() if args.note else ""
    log_mood(args.emoji, note_text, args.notify)

if __name__ == "__main__":
    main()
