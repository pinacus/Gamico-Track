# Gamico Track

A lightweight desktop app that watches Steam game prices and emails you the moment a game drops to (or below) the price you set. Built with Python and CustomTkinter, backed by the CheapShark and Steam Storefront APIs, with Google Sheets as the data store.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-00ADB5" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/status-in%20development-yellow" alt="Status">
</p>

## What it does

1. You type a game title and your target price into the app.
2. Gamico Track looks up the game on **CheapShark**, resolves its Steam App ID, and fetches the current price from the **Steam Storefront API**.
3. The entry is saved to a **Google Sheet** (via the [Sheety](https://sheety.co) API), acting as your watchlist.
4. A backend check (run manually or on a schedule) re-fetches the current price for every game in the sheet, updates the sheet, and sends you an **email via Gmail SMTP** for any game that has hit your target price.

## Features

- Simple GUI for adding games and target prices — no spreadsheet editing required
- Automatic game resolution via CheapShark (title → CheapShark ID → Steam App ID)
- Live Steam price lookups (India region pricing by default via `cc=in`)
- Google Sheets as a free, human-readable backend (no database needed)
- Email alerts sent through Gmail SMTP when a tracked game hits your price
- In-app config popup for setting your Sheety API URL and Gmail app credentials

## Tech stack

| Piece | Tool |
|---|---|
| GUI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Game data | [CheapShark API](https://apidocs.cheapshark.com/) |
| Pricing data | Steam Storefront API |
| Storage | Google Sheets, via [Sheety](https://sheety.co) |
| Notifications | Gmail SMTP (`smtplib`) |

## Project structure

```
Gamico Track/
├── main.py                   # Entry point — launches the GUI
├── notification_manager.py   # Re-checks prices for all saved games, sends email alerts
├── backend_process.py        # Standalone runner for notification_manager (for scheduling)
├── game_search.py            # CheapShark + Steam price lookups
├── GUI/
│   ├── GUI.py                # Main window + config popup
│   ├── data.json             # Local config (email, Sheety URL, Gmail app credentials)
│   └── logo.png              # App logo (click it to open config)
└── Sheet/
    └── google_sheet.py       # Sheety API wrapper (GET / POST / PUT)
```

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/pinacus/gamico-track.git
cd gamico-track
pip install customtkinter pillow word2number requests
```

### 2. Create a Google Sheet + Sheety endpoint

1. Create a Google Sheet with a `sheet1` tab containing these columns: `date`, `gameTitle`, `targetPrice`, `currentPrice`, `gameId`.
2. Connect it to [Sheety](https://sheety.co) to get an API endpoint URL.

### 3. Generate a Gmail App Password

Since Gmail blocks regular password SMTP login, you'll need an [App Password](https://support.google.com/accounts/answer/185833) tied to a Google account with 2FA enabled.

### 4. Run the app

```bash
python main.py
```

Click the logo in the top of the window to open the **config popup**, where you'll enter:

- Your Sheety API URL
- Your Gmail address (used to send alerts)
- Your Gmail App Password

Then fill in the main form with the game title, your email (where alerts go), and your target price, and hit **Save**.

### 5. Run price checks

`notification_manager.py` pulls every row from your sheet, re-checks the Steam price, updates the sheet, and emails you for any game at or under target price. Run it manually:

```bash
python "Gamico Track/backend_process.py"
```

...or schedule it (cron, Task Scheduler, systemd timer, etc.) to run periodically for automatic monitoring.

## Note
- Steam pricing is fetched for the `in` (India) region by default; edit the `cc` param in `game_search.py` / `notification_manager.py` to change this.

## License

MIT
