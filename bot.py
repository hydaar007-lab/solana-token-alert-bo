import requests
import time
import os

# -----------------------------
# CONFIGURATION
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))
SEEN = set()
CHAIN = "solana"
CHECK_INTERVAL = 60
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

                detail = get_coin_detail(coin_id)
                links = detail.get("links", {})
                homepage = links.get("homepage", ["Not Available"])[0]
                telegram = links.get("telegram_channel_identifier", "Not Available")
                twitter = links.get("twitter_screen_name", "Not Available")

                tg_link = f"https://t.me/{telegram}" if telegram != "Not Available" and telegram else "Not Available"
                x_link = f"https://x.com/{twitter}" if twitter != "Not Available" and twitter else "Not Available"

                message = (
                    f"🔔 *NEW TOKEN:* {coin['name']} `{contract_address[:6]}...{contract_address[-4:]}`\n"
                    f"⛓️ *Chain:* {CHAIN.upper()}\n\n"
                    f"🌐 *Website:* {homepage}\n"
                    f"✈️ *Telegram:* {tg_link}\n"
                    f"🐦 *Twitter (X):* {x_link}\n"
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
            print(f"Error during check: {e}")
        print(f"Sleeping {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL)
