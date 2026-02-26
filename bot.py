import requests
import time
import os

# -----------------------------
# CONFIGURATION
BOT_TOKEN = os.environ.get(8733379389:AAFX21XoAKv-TD0uLNnFLz0sl-yRpATDKk8)
CHAT_ID = int(os.environ.get(-1003692871546)
SEEN = set()
CHAIN = "solana"  # Solana platform
CHECK_INTERVAL = 60  # seconds
# -----------------------------

def send_telegram(msg):
    """Send a formatted message to the Telegram group."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Telegram send error:", e)

def get_coingecko_list():
    """Fetch the full list of coins from CoinGecko with platforms."""
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    return requests.get(url).json()

def get_coin_detail(coin_id):
    """Fetch detailed coin info from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    return requests.get(url).json()

def check_new_tokens():
    """Check for new tokens on the specified chain and alert Telegram."""
    all_coins = get_coingecko_list()
    for coin in all_coins:
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
                message = (
                    f"🔔 *NEW TOKEN:* {coin['name']} `{contract_address[:6]}...{contract_address[-4:]}`\n"
                    f"⛓️ *Chain:* {CHAIN.upper()}\n\n"
                    f"🌐 *Website:* {homepage}\n"
                    f"📊 *Chart:* https://dexscreener.com/{CHAIN}/{contract_address}\n"
                    f"📝 *Contract:* `{contract_address}`"
                )

                send_telegram(message)
                print(f"Sent alert for {coin['name']}")

# -----------------------------
# RUN LOOP
# -----------------------------
if __name__ == "__main__":
    print("Bot started. Monitoring new tokens...")
    while True:
        try:
            check_new_tokens()
        except Exception as e:
            print("Error:", e)
        time.sleep(CHECK_INTERVAL)
