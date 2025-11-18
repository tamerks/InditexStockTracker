#!/usr/bin/env python3
"""
Sahibinden.com scraper test scripti
"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scraperHelpers import scrape_sahibinden_list, scrape_sahibinden_list_with_details
import json

def setup_chrome_driver():
    """Chrome driver setup"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {e}")
        return None

def main():
    """Test sahibinden.com scraper"""
    # Test URL'i - komut satırından al veya varsayılan kullan
    # --details veya -d flag'i ile detay bilgileri de çekilir
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--") and not arg.startswith("-")]
    flags = [arg for arg in sys.argv[1:] if arg.startswith("--") or arg.startswith("-")]
    
    test_url = args[0] if args else "https://www.sahibinden.com/audi"
    fetch_details = "--details" in flags or "-d" in flags
    
    print(f"🧪 Testing sahibinden.com scraper")
    print(f"🔗 URL: {test_url}")
    if fetch_details:
        print(f"📋 Mode: With details (first 5 listings)")
    else:
        print(f"📋 Mode: List only")
    print("-" * 60)
    
    driver = setup_chrome_driver()
    if not driver:
        print("❌ Failed to setup Chrome driver")
        return
    
    try:
        print("📡 Loading page...")
        driver.get(test_url)
        
        # Detay bilgileri isteniyor mu kontrol et (main'de zaten kontrol edildi)
        max_details = 5  # Varsayılan olarak 5 ilanın detayını çek
        
        if fetch_details:
            print("🔍 Scraping listings with details...")
            listings = scrape_sahibinden_list_with_details(driver, max_details=max_details)
        else:
            print("🔍 Scraping listings...")
            listings = scrape_sahibinden_list(driver)
        
        print("\n" + "=" * 60)
        print(f"✅ Found {len(listings)} listings")
        print("=" * 60)
        
        if listings:
            print("\n📋 İlan Listesi:\n")
            for i, listing in enumerate(listings[:20], 1):  # İlk 20 ilanı göster
                print(f"{i}. {listing.get('title', 'N/A')}")
                print(f"   💰 Fiyat: {listing.get('price', 'N/A')}")
                print(f"   📍 Lokasyon: {listing.get('location', 'N/A')}")
                
                # Detay bilgileri varsa göster
                if listing.get('model_year'):
                    print(f"   📅 Model Yılı: {listing.get('model_year')}")
                if listing.get('kilometer'):
                    print(f"   🛣️  Kilometre: {listing.get('kilometer')}")
                if listing.get('transmission'):
                    print(f"   ⚙️  Vites: {listing.get('transmission')}")
                if listing.get('fuel_type'):
                    print(f"   ⛽ Yakıt: {listing.get('fuel_type')}")
                if listing.get('engine_power'):
                    print(f"   🔧 Motor: {listing.get('engine_power')}")
                if listing.get('color'):
                    print(f"   🎨 Renk: {listing.get('color')}")
                if listing.get('body_type'):
                    print(f"   🚗 Kasa: {listing.get('body_type')}")
                if listing.get('photo_count'):
                    print(f"   📸 Fotoğraf: {listing.get('photo_count')} adet")
                if listing.get('description'):
                    desc = listing.get('description', '')[:100]
                    print(f"   📝 Açıklama: {desc}...")
                
                print(f"   🔗 URL: {listing.get('url', 'N/A')}")
                print()
            
            # JSON olarak kaydet
            output_file = "sahibinden_test_results.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(listings, f, ensure_ascii=False, indent=2)
            print(f"💾 Results saved to: {output_file}")
        else:
            print("⚠️ No listings found!")
            print("\n💡 Debugging tips:")
            print("   - Sayfanın yüklenmesini bekleyin")
            print("   - Sahibinden.com'un HTML yapısı değişmiş olabilir")
            print("   - Selector'ları kontrol edin")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔄 Closing browser...")
        driver.quit()
        print("✅ Test completed!")

if __name__ == "__main__":
    main()

