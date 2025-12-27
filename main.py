import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Pygame not properly installed. Audio alerts will be disabled.")
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import requests
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

with open("config.json", "r") as config_file:
    config = json.load(config_file)

urls_to_check = config["urls"]
sleep_min_seconds = config["sleep_min_seconds"]
sleep_max_seconds = config["sleep_max_seconds"]

if PYGAME_AVAILABLE:
    pygame.mixer.init()

cart_status = {item["url"]: False for item in urls_to_check}

# Bot message fetch variables:
load_dotenv()
BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Foolproof for not having .env and bot installed: 
TELEGRAM_ENABLED = False
if BOT_API and CHAT_ID:
    TELEGRAM_ENABLED = True
else:
    print("BOT_API or CHAT_ID not found in .env file. Telegram messages will be disabled.")

DISCORD_ENABLED = False
if DISCORD_WEBHOOK_URL:
    DISCORD_ENABLED = True
    print("Discord Webhook found. Discord messages will be enabled.")
else:
    print("DISCORD_WEBHOOK_URL not found in .env file. Discord messages will be disabled.")

# This fcn is for notification sound
def play_sound(sound_file):
    if not PYGAME_AVAILABLE:
        print(f"🎵 (Audio disabled) Sound alert would play: {sound_file}")
        return
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

# This fcn is for sending messages
def send_telegram_message(message):
    if not TELEGRAM_ENABLED:
        print("⚠️ Telegram message skipped (missing BOT_API or CHAT_ID).")
        return

    url = f"https://api.telegram.org/bot{BOT_API}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("Telegram message sent.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

# This fcn is for sending Discord messages
def send_discord_message(message):
    if not DISCORD_ENABLED:
        return

    payload = {
        "content": message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        print("Discord message sent.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord message: {e}")

while True:
    # Crate service & initialize
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # modern headless mode
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for item in urls_to_check:
            try:
                if cart_status[item["url"]]:
                    print("Item already in cart, skipping...")
                    continue
                else:
                    url = item.get("url")
                    store = item.get("store")
                    sizes_to_check = item.get("sizes", [])
                    person = item.get("person", "Bilinmeyen")
                    driver.get(url)
                    print("--------------------------------")
                    print(f"Url {url} için ({person}): ")
                    if store == "zara":
                        # Check stock for the specified sizes
                        size_in_stock = check_stock_zara(driver, sizes_to_check)
                        if size_in_stock:
                            message = f"🛍️{size_in_stock} beden stokta!!!!\n👤Kişi: {person}\nLink: {url}"
                            print(f"ALERT: {message}")
                            play_sound('Crystal.mp3')
                            send_telegram_message(message)
                            send_discord_message(message)
                            cart_status[url] = True
                        else:
                            print(f"Checked {url} - no stock found for sizes {', '.join(sizes_to_check)}.")
                    elif store == "bershka":
                        size_in_stock = check_stock_bershka(driver, sizes_to_check)
                        if size_in_stock:
                            message = f"🛍️{size_in_stock} beden stokta!!!!\n👤Kişi: {person}\nLink: {url}"
                            print(f"ALERT: {message}")
                            play_sound('Crystal.mp3')
                            send_telegram_message(message)
                            send_discord_message(message)
                            cart_status[url] = True
                        else:
                            print(f"Checked {url} - no stock found for sizes {', '.join(sizes_to_check)}.")
                    elif store == "stradivarius":
                        size_in_stock = check_stock_stradivarius(driver, sizes_to_check)
                        if size_in_stock:
                            message = f"🛍️{size_in_stock} beden stokta!!!!\n👤Kişi: {person}\nLink: {url}"
                            print(f"ALERT: {message}")
                            play_sound('Crystal.mp3')
                            send_telegram_message(message)
                            send_discord_message(message)
                            cart_status[url] = True
                        else:
                            print(f"Checked {url} - no stock found for sizes {', '.join(sizes_to_check)}.")
                    else:
                        print("Store not supported")
            except Exception as e:
                print(f"An error occurred with URL {url}: {e}")
    finally:
        print("Closing the browser...")
        driver.quit()

        # Sleep for a random time between the specified min and max seconds before the next check
        sleep_time = random.randint(sleep_min_seconds, sleep_max_seconds)
        print(f"Sleeping for {sleep_time // 60} minutes and {sleep_time % 60} seconds...")
        time.sleep(sleep_time)
