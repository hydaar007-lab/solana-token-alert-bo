import requests
import time

# -----------------------------
# CONFIGURATION
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
SEEN = set()
CHAIN = "solana"  # Solana platform
# -----------------------------

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def get_coingecko_list():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    return requests.get(url).json()

def get_coin_detail(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    return requests.get(url).json()

def check_new_tokens():
    all_coins = get_coingecko_list()
    for coin in all_coins:
        # Only tokens on the specified chain
        if CHAIN in coin["platforms"] and coin["platforms"][CHAIN]:
            contract_address = coin["platforms"][CHAIN]
            coin_id = coin["id"]

            if coin_id not in SEEN:
                SEEN.add(coin_id)

                # Get extra details
                detail = get_coin_detail(coin_id)
                links = detail.get("links", {})
                homepage = links.get("homepage", ["Not Available"])[0]

                # Build message
                message = f"""
🔔 NEW TOKEN: {coin['name']} {contract_address[:6]}...{contract_address[-4:]}
⛓️ {CHAIN.upper()}

📱 Telegram: Join Group
🐦 Twitter: Follow
🌐 Website: {homepage}

📝 Contract:
{contract_address}

📊 Chart: https://dexscreener.com/{CHAIN}/{contract_address}
"""

                send_telegram(message)
                print(f"Sent alert for {coin['name']}")

# -----------------------------
# RUN LOOP
# -----------------------------
while True:
    try:
        check_new_tokens()
    except Exception as e:
        print("Error:", e)
    time.sleep(60)  # check every 60 seconds
