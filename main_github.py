import json
import time
import random
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
    """Chrome driver setup for GitHub Actions"""
    chrome_options = Options()
    
    # GitHub Actions için optimize edilmiş ayarlar
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")  # Performans için
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Memory optimization
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    chrome_options.add_argument("--disable-background-timer-throttling")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)  # 30 saniye timeout
        return driver
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {e}")
        return None

def check_single_item(driver, item, sizes_to_check, telegram_enabled, bot_api, chat_id):
    """Tek item için stok kontrolü"""
    try:
        url = item.get("url")
        store = item.get("store", "").lower()
        
        if not url or not store:
            print("⚠️ Invalid item configuration")
            return False
            
        print(f"\n📋 Checking: {store.upper()} - {url}")
        
        # Driver'ı sayfaya yönlendir
        driver.get(url)
        
        # Kısa bekleme (sayfa yüklenmesi için)
        time.sleep(random.uniform(2, 4))
        
        size_in_stock = None
        
        # Store'a göre stok kontrolü
        if store == "zara":
            size_in_stock = check_stock_zara(driver, sizes_to_check)
        elif store == "bershka":
            size_in_stock = check_stock_bershka(driver, sizes_to_check)
        elif store == "stradivarius":
            size_in_stock = check_stock_stradivarius(driver, sizes_to_check)
        else:
            print(f"❌ Unsupported store: {store}")
            return False
            
        if size_in_stock:
            message = f"🛍️ <b>STOK BULUNDU!</b>\n\n" \
                     f"📏 Beden: <b>{size_in_stock}</b>\n" \
                     f"🏪 Mağaza: <b>{store.upper()}</b>\n" \
                     f"🔗 <a href='{url}'>Ürün Linki</a>\n" \
                     f"⏰ Zaman: {time.strftime('%H:%M:%S')}"
            
            print(f"🎉 ALERT: {message}")
            
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
    """Ana fonksiyon - GitHub Actions için tek çalışım"""
    print("🚀 Starting Zara Stock Checker (GitHub Actions)")
    print(f"⏰ Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Config yükle
    config = load_config()
    if not config:
        print("❌ Failed to load configuration")
        return
        
    urls_to_check = config.get("urls", [])
    sizes_to_check = config.get("sizes_to_check", [])
    
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
                driver, item, sizes_to_check, 
                telegram_enabled, bot_api, chat_id
            )
            
            if result:
                found_stock = True
                
            # Items arası kısa bekleme
            if checked_count < len(urls_to_check):
                wait_time = random.uniform(3, 7)
                print(f"⏳ Waiting {wait_time:.1f} seconds before next check...")
                time.sleep(wait_time)
                
    except KeyboardInterrupt:
        print("\n⏹️ Stock checker stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        print("\n🔄 Closing browser...")
        driver.quit()
        
    # Özet
    print(f"\n{'='*50}")
    print("📊 SUMMARY")
    print(f"✅ Items checked: {checked_count}")
    print(f"🛍️ Stock found: {'YES' if found_stock else 'NO'}")
    print(f"⏰ End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏁 Stock check completed")
    
    # Telegram'a özet gönder (sadece stok bulunmazsa)
    if telegram_enabled and not found_stock:
        summary_message = f"📊 <b>Stok Kontrolü Tamamlandı</b>\n\n" \
                         f"✅ Kontrol edilen ürün: {checked_count}\n" \
                         f"❌ Stok bulunamadı\n" \
                         f"⏰ {time.strftime('%H:%M:%S')}"
        send_telegram_message(summary_message, bot_api, chat_id)

if __name__ == "__main__":
    main() 