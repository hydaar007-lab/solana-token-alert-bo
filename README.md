# Solana Token Alert Bot

This bot detects newly added Solana tokens (via CoinGecko API) and sends formatted alerts to your Telegram group.

## Setup

1. Create Telegram bot via BotFather  
2. Get your chat ID  
3. Replace `BOT_TOKEN` and `CHAT_ID` in `bot.py`  

## Deployment (Free on Render.com)

1. Create free account on [Render.com](https://render.com)  
2. Connect your GitHub repo  
3. New → Web Service → Python 3  
4. Build command: `pip install -r requirements.txt`  
5. Start command: `python bot.py`  
6. Deploy!

## Features

- Alerts for new tokens on Solana chain  
- Sends Telegram message with contract, chart, and website  
- Free API (CoinGecko)  
- Auto-check every 60 seconds
