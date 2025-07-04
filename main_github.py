import json
import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

def load_config():
    """Config dosyasını yükle"""
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("❌ config.json file not found!")
        return None

def save_config(config):
    """Config dosyasını kaydet ve GitHub'a push et"""
    try:
        # Dosyayı kaydet
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=2, ensure_ascii=False)
        
        # GitHub Actions'ta Git konfigürasyonu ve push
        if os.getenv('GITHUB_ACTIONS'):
            try:
                # Git config
                subprocess.run(['git', 'config', '--global', 'user.name', 'Stock Checker Bot'], check=True, capture_output=True)
                subprocess.run(['git', 'config', '--global', 'user.email', 'actions@github.com'], check=True, capture_output=True)
                
                # Changes add, commit ve push
                subprocess.run(['git', 'add', 'config.json'], check=True, capture_output=True)
                
                # Check if there are changes to commit
                result = subprocess.run(['git', 'diff', '--staged', '--quiet'], capture_output=True)
                if result.returncode != 0:  # There are changes
                    commit_msg = f"🗑️ Auto-remove found item - {time.strftime('%H:%M:%S')}"
                    subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
                    subprocess.run(['git', 'push'], check=True, capture_output=True)
                    print("✅ Config changes pushed to GitHub")
                    return True
                else:
                    print("⚠️ No config changes to commit")
                    return True
                    
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Git operation failed: {e}")
                return True  # Config file still saved locally
        else:
            print("✅ Config saved locally")
            return True
            
    except Exception as e:
        print(f"❌ Config save failed: {e}")
        return False

def remove_item_from_config(config, item_to_remove):
    """Stok bulunan ürünü config'den çıkar"""
    try:
        original_count = len(config.get("urls", []))
        config["urls"] = [item for item in config.get("urls", []) if item["url"] != item_to_remove["url"]]
        removed = original_count - len(config["urls"])
        
        if removed > 0:
            print(f"🗑️ Removed {removed} item from config (stock found)")
            return save_config(config)
        return False
    except Exception as e:
        print(f"❌ Remove item error: {e}")
        return False

def setup_telegram():
    """Telegram credentials setup"""
    BOT_API = os.getenv("BOT_API")
    CHAT_ID = os.getenv("CHAT_ID")
    
    if not BOT_API or not CHAT_ID:
        print("⚠️ BOT_API or CHAT_ID not found in environment variables. Telegram messages will be disabled.")
        return False, None, None
    
    return True, BOT_API, CHAT_ID

def send_telegram_message(message, bot_api, chat_id):
    """Telegram message gönder"""
    if not bot_api or not chat_id:
        print("⚠️ Telegram message skipped (missing credentials).")
        return False

    url = f"https://api.telegram.org/bot{bot_api}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("✅ Telegram message sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False

def setup_chrome_driver():
    """Super fast Chrome driver setup for GitHub Actions"""
    chrome_options = Options()
    
    # Maximum speed optimization
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    # JavaScript'i tamamen kapatmak Zara için sorunlu - sadece resim ve CSS'i kapat
    chrome_options.add_argument("--disable-fonts")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--safebrowsing-disable-auto-update")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1280,720")  # Smaller window
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Memory limits
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=2048")  # Lower memory
    
    try:
        # Skip ChromeDriverManager for speed, use system chrome
        service = Service('/usr/bin/chromedriver') if os.path.exists('/usr/bin/chromedriver') else Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(15)  # Faster timeout
        driver.implicitly_wait(5)  # Faster implicit wait
        return driver
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {e}")
        return None

def check_single_item(driver, item, telegram_enabled, bot_api, chat_id, config):
    """Tek item için stok kontrolü"""
    try:
        url = item.get("url")
        store = item.get("store", "").lower()
        sizes_to_check = item.get("sizes", [])
        person = item.get("person", "Bilinmeyen")
        
        if not url or not store:
            print("⚠️ Invalid item configuration")
            return False
            
        print(f"\n📋 Checking: {store.upper()} - {url} ({person})")
        
        # Driver'ı sayfaya yönlendir
        driver.get(url)
        
        # Minimal bekleme (speed optimization)
        time.sleep(random.uniform(1, 2))
        
        size_in_stock = None
        
        # Store'a göre stok kontrolü - timeout'a karşı robust error handling
        try:
            if store == "zara":
                size_in_stock = check_stock_zara(driver, sizes_to_check)
            elif store == "bershka":
                size_in_stock = check_stock_bershka(driver, sizes_to_check)
            elif store == "stradivarius":
                size_in_stock = check_stock_stradivarius(driver, sizes_to_check)
            else:
                print(f"❌ Unsupported store: {store}")
                return False
        except Exception as e:
            print(f"⚠️ Store checker failed for {store}: {e}")
            size_in_stock = None
            
        if size_in_stock:
            # Ürünü config'den çıkar (sürekli bildirim gelmesin)
            removed = remove_item_from_config(config, item)
            
            auto_remove_msg = "🗑️ Ürün takip listesinden çıkarıldı" if removed else "⚠️ Manuel listeden çıkarmanız gerekiyor"
            
            message = f"🛍️ <b>STOK BULUNDU!</b>\n\n" \
                     f"👤 Kişi: <b>{person}</b>\n" \
                     f"📏 Beden: <b>{size_in_stock}</b>\n" \
                     f"🏪 Mağaza: <b>{store.upper()}</b>\n" \
                     f"🔗 <a href='{url}'>Ürün Linki</a>\n" \
                     f"⏰ Zaman: {time.strftime('%H:%M:%S')}\n\n" \
                     f"{auto_remove_msg}"
            
            print(f"🎉 STOCK FOUND: {size_in_stock} - {store.upper()}")
            print(f"🗑️ Auto-removed from list: {removed}")
            
            if telegram_enabled:
                send_telegram_message(message, bot_api, chat_id)
            
            return True
        else:
            print(f"❌ No stock found for sizes: {', '.join(sizes_to_check)}")
            return False
            
    except TimeoutException:
        print(f"⏱️ Timeout while checking {url}")
        return False
    except WebDriverException as e:
        print(f"🌐 WebDriver error for {url}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking {url}: {e}")
        return False

def main():
    """Super Fast Stock Checker - GitHub Actions Optimized"""
    print("⚡ SUPER FAST Stock Checker (Every 5 min)")
    print(f"🚀 Start: {time.strftime('%H:%M:%S')}")
    
    # Config yükle
    config = load_config()
    if not config:
        print("❌ Failed to load configuration")
        return
        
    urls_to_check = config.get("urls", [])
    
    if not urls_to_check:
        print("❌ No URLs to check in configuration")
        return
        
    # Telegram setup
    telegram_enabled, bot_api, chat_id = setup_telegram()
    
    # Chrome driver setup
    driver = setup_chrome_driver()
    if not driver:
        print("❌ Failed to setup Chrome driver")
        return
        
    found_stock = False
    checked_count = 0
    
    try:
        for item in urls_to_check:
            checked_count += 1
            print(f"\n{'='*50}")
            print(f"📦 Item {checked_count}/{len(urls_to_check)}")
            
            result = check_single_item(
                driver, item, 
                telegram_enabled, bot_api, chat_id, config
            )
            
            if result:
                found_stock = True
                
            # Items arası minimal bekleme (speed optimization)
            if checked_count < len(urls_to_check):
                wait_time = random.uniform(1, 2)
                print(f"⚡ Fast transition in {wait_time:.1f}s...")
                time.sleep(wait_time)
                
    except KeyboardInterrupt:
        print("\n⏹️ Stock checker stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        print("\n🔄 Closing browser...")
        driver.quit()
        
    # Fast summary
    remaining_items = len(config.get("urls", []))
    print(f"\n⚡ FAST SUMMARY")
    print(f"✅ Checked: {checked_count} | 🛍️ Found: {'YES' if found_stock else 'NO'}")
    print(f"📋 Remaining items: {remaining_items} | ⏱️ End: {time.strftime('%H:%M:%S')}")
    print(f"🏁 Next check in 5min" if remaining_items > 0 else "🎯 All items found - add new items to config.json")
    
    # Telegram summary and special cases
    if telegram_enabled:
        current_minute = int(time.strftime('%M'))
        
        # If no items left, send completion message
        if remaining_items == 0:
            completion_message = f"🎯 <b>Tüm Ürünler Bulundu!</b>\n\n" \
                               f"✅ Checked: {checked_count} items\n" \
                               f"🛍️ All stocks found and removed\n" \
                               f"📝 Add new items to config.json\n" \
                               f"⏰ {time.strftime('%H:%M')}"
            send_telegram_message(completion_message, bot_api, chat_id)
        
        # Send hourly summary only if items remain and no stock found
        elif not found_stock and (current_minute % 60 == 0):
            summary_message = f"⚡ <b>Hourly Stock Summary</b>\n\n" \
                             f"✅ System running every 5 min\n" \
                             f"📋 {remaining_items} items being tracked\n" \
                             f"❌ No stock found this hour\n" \
                             f"⏰ {time.strftime('%H:%M')}"
            send_telegram_message(summary_message, bot_api, chat_id)

if __name__ == "__main__":
    main() 