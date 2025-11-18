from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
import sys
import re

# Function to check stock availability (For ZARA)
def check_stock_zara(driver, sizes_to_check):
    try:
        # GitHub Actions için daha kısa timeout
        is_github_actions = os.getenv('GITHUB_ACTIONS')
        timeout = 10 if is_github_actions else 60
        wait = WebDriverWait(driver, timeout)

        # Close the cookie alert if it appears
        try:
            print("Checking for cookie alert...")
            cookie_wait = WebDriverWait(driver, 5)  # Cookie için kısa timeout
            accept_cookies_button = cookie_wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_cookies_button.click()
            print("Cookie alert closed successfully.")
        except TimeoutException:
            print("Cookie alert not found or already closed.")

        # Wait for "Add to Cart" button to be clickable
        try:
            add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-qa-action='add-to-cart']")))

            # Check if an overlay is blocking the button
            overlays = driver.find_elements(By.CLASS_NAME, "zds-backdrop")
            if overlays:
                print("Overlay detected. Attempting to remove it...")
                driver.execute_script("arguments[0].remove();", overlays[0])  # Remove overlay with JS

            # Click "Add to Cart" using JavaScript to bypass any hidden overlays
            driver.execute_script("arguments[0].click();", add_to_cart_button)
            print("Clicked 'Add to Cart' button.")
        except (TimeoutException, ElementClickInterceptedException) as e:
            print(f"Failed to click 'Add to Cart' button: {e}")
            return None

        # Wait for the size selector to appear
        print("Waiting for sizes to appear...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "size-selector-sizes")))

        # Find size elements
        size_elements = driver.find_elements(By.CLASS_NAME, "size-selector-sizes-size")
        sizes_found = {size: False for size in sizes_to_check}

        for li in size_elements:
            try:
                size_label = li.find_element(By.CSS_SELECTOR, "div[data-qa-qualifier='size-selector-sizes-size-label']").text.strip()
                if size_label in sizes_to_check:
                    sizes_found[size_label] = True
                    button = li.find_element(By.CLASS_NAME, "size-selector-sizes-size__button")

                    # Check if the button contains "Benzer ürünler" text
                    try:
                        similar_products_text = button.find_element(By.CLASS_NAME, "size-selector-sizes-size__action").text.strip()
                        if "Benzer ürünler" in similar_products_text:
                            print(f"The {size_label} size is out of stock and showing similar products.")
                            return False
                    except NoSuchElementException:
                        pass  # No "Benzer ürünler" text found, proceed with normal check

                    # Check stock status
                    if button.get_attribute("data-qa-action") in ["size-in-stock", "size-low-on-stock"]:
                        print(f"The {size_label} size is in stock.")
                        return size_label
                    else:
                        print(f"The {size_label} size is out of stock.")
                        return False
            except Exception as e:
                print(f"Error processing size element: {e}")
                continue

        if not any(sizes_found.values()):
            print(f"Sizes {', '.join(sizes_to_check)} not found.")
    except Exception as e:
        print(f"An error occurred during the operation: {e}")

    return None

# Function to check stock availability (For Rossmann)
def rossmannStockCheck(driver):
    wait = WebDriverWait(driver, 40)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-add-form")))
    except Exception:
        print(f"Yok yok bu ürün")
        return False
    try:
        # Locate the button with the text "Sepete Ekle"
        button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'Sepete Ekle')]")
        if button:
            print("Rossmann ürünü stokta")
            print("Sepete eklendi!")
            driver.execute_script("arguments[0].click();", button)
            return True
    except Exception:
        print(f"Yok yok bu ürün anla yok kalmamış")
    return False


def check_stock_bershka(driver, sizes_to_check):
    try:
        # GitHub Actions için optimize edilmiş timeout
        is_github_actions = os.getenv('GITHUB_ACTIONS')
        timeout = 8 if is_github_actions else 10
        wait = WebDriverWait(driver, timeout)

        # Handle cookie popup if present
        try:
            print("Checking for cookie alert...")
            cookie_wait = WebDriverWait(driver, 3)  # Cookie için kısa timeout
            accept_cookies_button = cookie_wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_cookies_button.click()
            print("Cookie alert closed.")
        except Exception:
            print("No cookie alert or already closed.")

        # Wait for the size list to load
        print("Waiting for the size list...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-anchor='productDetailSize']")))

        # Allow extra time for dynamic class updates to finish
        time.sleep(3)  # Give JS time to update classes (can be adjusted or replaced by smarter wait below)

        size_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-qa-anchor='sizeListItem']")
        sizes_found = {size: False for size in sizes_to_check}

        for button in size_buttons:
            try:
                size_label_elem = button.find_element(By.CSS_SELECTOR, "span.text__label")
                size_label = size_label_elem.text.strip()

                if size_label in sizes_to_check:
                    sizes_found[size_label] = True

                    # Wait for the class to include 'is-disabled' or not
                    def class_stabilized(driver):
                        cls = button.get_attribute("class")
                        return "is-disabled" in cls or "is-disabled" not in cls

                    WebDriverWait(driver, 5).until(class_stabilized)

                    class_attr = button.get_attribute("class")
                    if "is-disabled" in class_attr:
                        print(f"{size_label} is out of stock.")
                    else:
                        print(f"{size_label} is in stock!")
                        return size_label
            except Exception as e:
                print(f"Error processing size button: {e}")
                continue

        if not any(sizes_found.values()):
            print(f"⚠️ Sizes {', '.join(sizes_to_check)} not found.")
    except Exception as e:
        print(f"An error occurred while checking Bershka stock: {e}")

    return None
    
def watsonsChecker(driver):
    wait = WebDriverWait(driver, 40)
    try:
        element = wait.until(EC.presence_of_all_elements_located(By.CLASS_NAME, "product-grid-manager__view-mount"))
        text = element.text.strip()
        return not ("0 ürün") in text
    except:
        return False

def check_stock_stradivarius(driver, sizes_to_check):
    try:
        # GitHub Actions için optimize edilmiş timeout
        is_github_actions = os.getenv('GITHUB_ACTIONS')
        timeout = 10 if is_github_actions else 60
        wait = WebDriverWait(driver, timeout)
        
        # Close the cookie alert if it appears
        try:
            print("Checking for cookie alert...")
            cookie_wait = WebDriverWait(driver, 5)  # Cookie için kısa timeout
            accept_cookies_button = cookie_wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_cookies_button.click()
            print("Cookie alert closed successfully.")
        except TimeoutException:
            print("Cookie alert not found or already closed.")

        # Try to find and click size selector button or add to cart
        try:
            # Look for add to cart or size selector button
            add_to_cart_selectors = [
                "button[data-qa-action='add-to-cart']",
                ".product-detail-actions__add-to-cart",
                ".add-to-cart-button",
                ".product-actions__add-to-cart",
                "button[class*='add-to-cart']"
            ]
            
            add_to_cart_button = None
            for selector in add_to_cart_selectors:
                try:
                    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except TimeoutException:
                    continue
            
            if add_to_cart_button:
                # Click "Add to Cart" using JavaScript to bypass any hidden overlays
                driver.execute_script("arguments[0].click();", add_to_cart_button)
                print("Clicked 'Add to Cart' button.")
            else:
                print("Add to cart button not found")
                return None
        except Exception as e:
            print(f"Failed to click 'Add to Cart' button: {e}")
            return None

        # Wait for the size selector to appear
        print("Waiting for sizes to appear...")
        time.sleep(2)  # Give some time for size selector to load
        
        # Try different size selector patterns for Stradivarius
        size_selectors = [
            ".size-selector-sizes-size",  # Zara-like
            ".product-size-selector__item",  # Common pattern
            ".size-list__item",
            "[data-qa*='size']",
            ".sizes__item"
        ]
        
        size_elements = []
        for selector in size_selectors:
            try:
                size_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if size_elements:
                    print(f"Found size elements with selector: {selector}")
                    break
            except Exception:
                continue
        
        if not size_elements:
            print("No size elements found")
            return None

        sizes_found = {size: False for size in sizes_to_check}

        for element in size_elements:
            try:
                # Try different ways to get size text
                size_label = None
                size_text_selectors = [
                    "div[data-qa-qualifier='size-selector-sizes-size-label']",
                    ".size-label",
                    ".text__label", 
                    "span"
                ]
                
                for text_selector in size_text_selectors:
                    try:
                        size_label_elem = element.find_element(By.CSS_SELECTOR, text_selector)
                        size_label = size_label_elem.text.strip()
                        if size_label:
                            break
                    except:
                        continue
                
                # If no specific selector worked, try getting text directly
                if not size_label:
                    size_label = element.text.strip()
                
                if size_label in sizes_to_check:
                    sizes_found[size_label] = True
                    
                    # Try to find button within the element
                    button = None
                    button_selectors = [
                        ".size-selector-sizes-size__button",
                        "button",
                        "[role='button']"
                    ]
                    
                    for btn_selector in button_selectors:
                        try:
                            button = element.find_element(By.CSS_SELECTOR, btn_selector)
                            break
                        except:
                            continue
                    
                    if not button:
                        button = element  # Use the element itself if no button found
                    
                    # Check if size is available
                    element_classes = element.get_attribute("class") or ""
                    button_classes = button.get_attribute("class") or ""
                    
                    # Check for disabled/out of stock indicators
                    if any(indicator in element_classes.lower() or indicator in button_classes.lower() 
                           for indicator in ["disabled", "unavailable", "out-of-stock", "sold-out"]):
                        print(f"The {size_label} size is out of stock.")
                        continue
                    
                    # Check for available/in-stock indicators
                    data_qa = button.get_attribute("data-qa-action") or ""
                    if "stock" in data_qa or not any(indicator in data_qa for indicator in ["disabled", "unavailable"]):
                        print(f"The {size_label} size is in stock.")
                        return size_label
                        
            except Exception as e:
                print(f"Error processing size element: {e}")
                continue

        if not any(sizes_found.values()):
            print(f"Sizes {', '.join(sizes_to_check)} not found.")
            
    except Exception as e:
        print(f"An error occurred during Stradivarius stock check: {e}")

    return None

def scrape_sahibinden_list(driver):
    """
    Sahibinden.com sayfasındaki ilan listesini çeker ve döndürür.
    Returns: List of dictionaries containing listing information
    """
    try:
        is_github_actions = os.getenv('GITHUB_ACTIONS')
        timeout = 15 if is_github_actions else 30
        wait = WebDriverWait(driver, timeout)
        
        print("Waiting for sahibinden.com page to load...")
        
        # Cookie popup'ı kapatmaya çalış
        try:
            cookie_wait = WebDriverWait(driver, 5)
            # Sahibinden.com cookie butonları için farklı selector'lar dene
            cookie_selectors = [
                "button[id*='cookie']",
                "button[class*='cookie']",
                ".cookie-accept",
                "#onetrust-accept-btn-handler"
            ]
            for selector in cookie_selectors:
                try:
                    cookie_button = cookie_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    driver.execute_script("arguments[0].click();", cookie_button)
                    print("Cookie popup closed.")
                    time.sleep(1)
                    break
                except:
                    continue
        except:
            print("No cookie popup found or already closed.")
        
        # Sayfanın yüklenmesini bekle
        time.sleep(2)
        
        # İlan listesi için farklı selector'ları dene
        listing_selectors = [
            "tr[class*='searchResultsItem']",
            ".searchResultsItem",
            "tr[data-id]",
            ".classified-list-item",
            "div[class*='classified']"
        ]
        
        listings = []
        listing_elements = []
        
        for selector in listing_selectors:
            try:
                listing_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if listing_elements:
                    print(f"Found {len(listing_elements)} listings with selector: {selector}")
                    break
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                continue
        
        if not listing_elements:
            print("⚠️ No listing elements found. Trying alternative approach...")
            # Alternatif: sayfadaki tüm linkleri kontrol et
            try:
                all_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/ilan/']")
                print(f"Found {len(all_links)} potential listing links")
                if all_links:
                    # İlk birkaç linki kontrol et
                    for link in all_links[:10]:
                        try:
                            href = link.get_attribute("href")
                            text = link.text.strip()
                            if href and text:
                                listings.append({
                                    "title": text,
                                    "url": href,
                                    "price": "N/A",
                                    "location": "N/A"
                                })
                        except:
                            continue
            except Exception as e:
                print(f"Alternative approach failed: {e}")
        
        # Her ilan için bilgileri çek
        for element in listing_elements[:50]:  # İlk 50 ilanı al
            try:
                listing_data = {}
                
                # Başlık ve link - önce tüm linkleri bul, sonra doğru olanı seç
                all_links = element.find_elements(By.CSS_SELECTOR, "a")
                listing_url = None
                listing_title = None
                
                # /ilan/ içeren ve geçerli URL'yi bul
                for link in all_links:
                    href = link.get_attribute("href") or ""
                    # Geçerli bir ilan URL'si olmalı
                    if "/ilan/" in href and href != "#" and "sahibinden.com/ilan/" in href:
                        listing_url = href
                        # Başlık metnini al
                        link_text = link.text.strip()
                        if link_text:
                            listing_title = link_text
                        else:
                            # Title attribute'unu dene
                            link_title = link.get_attribute("title") or ""
                            if link_title:
                                listing_title = link_title
                        break
                
                # Eğer hala URL bulunamadıysa, data-href veya onclick'i kontrol et
                if not listing_url:
                    for link in all_links:
                        data_href = link.get_attribute("data-href") or ""
                        if "/ilan/" in data_href:
                            listing_url = data_href if data_href.startswith("http") else f"https://www.sahibinden.com{data_href}"
                            link_text = link.text.strip()
                            listing_title = link_text if link_text else link.get_attribute("title") or ""
                            break
                
                # URL'yi kaydet
                listing_data["url"] = listing_url or "N/A"
                
                # Başlığı belirle
                if listing_title:
                    listing_data["title"] = listing_title
                elif listing_url and "/ilan/" in listing_url:
                    # URL'den başlık çıkar
                    url_parts = listing_url.split("/")
                    if len(url_parts) >= 4:
                        # URL formatı: .../ilan/vasita-otomobil-audi-2024-a4-40tdi.../detay
                        url_title_part = url_parts[3]
                        # İlk birkaç kelimeyi al ve daha okunabilir yap
                        title_words = url_title_part.replace("-", " ").split()[:8]  # İlk 8 kelime
                        listing_data["title"] = " ".join(title_words).title()
                    else:
                        listing_data["title"] = "Başlık bulunamadı"
                else:
                    # Son çare: element'in text içeriğini al
                    element_text = element.text.strip()
                    listing_data["title"] = element_text[:100] if element_text else "Başlık bulunamadı"
                
                # Fiyat
                try:
                    price_elem = element.find_element(By.CSS_SELECTOR, "td[class*='searchResultsPrice']")
                    listing_data["price"] = price_elem.text.strip()
                except:
                    try:
                        price_elem = element.find_element(By.CSS_SELECTOR, ".price")
                        listing_data["price"] = price_elem.text.strip()
                    except:
                        listing_data["price"] = "N/A"
                
                # Lokasyon
                try:
                    location_elem = element.find_element(By.CSS_SELECTOR, "td[class*='searchResultsLocation']")
                    listing_data["location"] = location_elem.text.strip()
                except:
                    try:
                        location_elem = element.find_element(By.CSS_SELECTOR, ".location")
                        listing_data["location"] = location_elem.text.strip()
                    except:
                        listing_data["location"] = "N/A"
                
                # Sadece geçerli URL'ye sahip ilanları ekle
                if listing_data.get("url") and listing_data["url"] != "N/A":
                    listings.append(listing_data)
                    
            except Exception as e:
                print(f"Error processing listing element: {e}")
                continue
        
        print(f"✅ Successfully scraped {len(listings)} listings from sahibinden.com")
        return listings
        
    except TimeoutException:
        print("⏱️ Timeout while loading sahibinden.com page")
        return []
    except Exception as e:
        print(f"❌ Error scraping sahibinden.com: {e}")
        return []

def scrape_sahibinden_detail(driver, detail_url):
    """
    Sahibinden.com detay sayfasından ek bilgileri çeker.
    Returns: Dictionary containing detailed listing information
    """
    detail_info = {}
    
    try:
        # Detay sayfasına git
        driver.get(detail_url)
        time.sleep(2)  # Sayfanın yüklenmesini bekle
        
        # Cookie popup'ı kapat
        try:
            cookie_wait = WebDriverWait(driver, 3)
            cookie_selectors = [
                "button[id*='cookie']",
                "button[class*='cookie']",
                ".cookie-accept",
                "#onetrust-accept-btn-handler"
            ]
            for selector in cookie_selectors:
                try:
                    cookie_button = cookie_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    driver.execute_script("arguments[0].click();", cookie_button)
                    time.sleep(0.5)
                    break
                except:
                    continue
        except:
            pass
        
        # İlan detay bilgileri için farklı selector'ları dene
        detail_selectors = {
            "model_year": [
                "li:contains('Model Yılı')",
                "dt:contains('Model Yılı')",
                "[class*='modelYear']",
                "[data-label*='Model Yılı']"
            ],
            "kilometer": [
                "li:contains('Kilometre')",
                "dt:contains('Kilometre')",
                "[class*='kilometer']",
                "[data-label*='Kilometre']"
            ],
            "transmission": [
                "li:contains('Vites')",
                "dt:contains('Vites')",
                "[class*='transmission']",
                "[data-label*='Vites']"
            ],
            "fuel_type": [
                "li:contains('Yakıt')",
                "dt:contains('Yakıt')",
                "[class*='fuel']",
                "[data-label*='Yakıt']"
            ],
            "engine_power": [
                "li:contains('Motor Gücü')",
                "dt:contains('Motor Gücü')",
                "[class*='enginePower']",
                "[data-label*='Motor Gücü']"
            ],
            "color": [
                "li:contains('Renk')",
                "dt:contains('Renk')",
                "[class*='color']",
                "[data-label*='Renk']"
            ],
            "description": [
                "[class*='description']",
                "[class*='classifiedDescription']",
                ".classified-detail-text",
                "#classifiedDescription"
            ],
            "phone": [
                "[class*='phone']",
                "[data-phone]",
                ".classified-contact-phone"
            ],
            "city": [
                "[class*='city']",
                "[class*='location']",
                ".classified-location"
            ]
        }
        
        # Genel bilgi tablosunu bul - Sahibinden.com'un özellikler listesi
        try:
            # Özellikler listesi için farklı yapıları dene
            property_selectors = [
                "ul.classifiedInfoList li",
                ".classifiedInfoList li",
                "dl.classifiedInfoList dt",
                ".classified-detail-info li",
                "[class*='classified-info'] li"
            ]
            
            properties_found = False
            for selector in property_selectors:
                try:
                    property_items = driver.find_elements(By.CSS_SELECTOR, selector)
                    if property_items:
                        properties_found = True
                        for item in property_items:
                            item_text = item.text.strip()
                            if not item_text:
                                continue
                            
                            # Label ve value'yu ayır
                            if ":" in item_text:
                                parts = item_text.split(":", 1)
                                label = parts[0].strip()
                                value = parts[1].strip()
                            else:
                                # dt/dd yapısı varsa
                                try:
                                    dt = item.find_element(By.CSS_SELECTOR, "dt, .label, strong")
                                    dd = item.find_element(By.CSS_SELECTOR, "dd, .value, span")
                                    label = dt.text.strip()
                                    value = dd.text.strip()
                                except:
                                    continue
                            
                            # Model Yılı
                            if "Model Yılı" in label or "Model" in label:
                                if value:
                                    detail_info["model_year"] = value
                            
                            # Kilometre
                            if "Kilometre" in label or "Km" in label:
                                if value and "Kilometre" not in value:
                                    detail_info["kilometer"] = value
                            
                            # Vites
                            if "Vites" in label:
                                if value:
                                    detail_info["transmission"] = value
                            
                            # Yakıt
                            if "Yakıt" in label:
                                if value:
                                    detail_info["fuel_type"] = value
                            
                            # Motor Gücü / Motor Hacmi
                            if "Motor Gücü" in label or "Motor Hacmi" in label or ("Motor" in label and "Gücü" in label):
                                if value and "Motor" not in value:
                                    detail_info["engine_power"] = value
                            
                            # Renk
                            if "Renk" in label:
                                if value:
                                    detail_info["color"] = value
                            
                            # Kasa Tipi
                            if "Kasa" in label:
                                if value:
                                    detail_info["body_type"] = value
                            
                            # Çekiş
                            if "Çekiş" in label:
                                if value:
                                    detail_info["drive_type"] = value
                        
                        if properties_found:
                            break
                except:
                    continue
            
            # Eğer özellikler listesi bulunamadıysa, genel text araması yap
            if not properties_found:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                # Basit regex ile bilgileri çıkar
                import re
                
                # Model yılı (örn: 2020, 2021, etc.)
                year_match = re.search(r'(19|20)\d{2}', page_text[:2000])
                if year_match:
                    detail_info["model_year"] = year_match.group(0)
                
                # Kilometre (örn: 50.000 km, 100000 km)
                km_match = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*(?:km|Km|KM|kilometre)', page_text[:2000], re.IGNORECASE)
                if km_match:
                    detail_info["kilometer"] = km_match.group(1) + " km"
        except Exception as e:
            print(f"  ⚠️ Error extracting info table: {e}")
        
        # Açıklama metnini bul
        try:
            desc_selectors = [
                "[class*='classifiedDescription']",
                "[class*='description']",
                ".classified-detail-text",
                "#classifiedDescription",
                "[id*='description']"
            ]
            for selector in desc_selectors:
                try:
                    desc_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    description = desc_elem.text.strip()
                    if description and len(description) > 20:
                        detail_info["description"] = description[:500]  # İlk 500 karakter
                        break
                except:
                    continue
        except Exception as e:
            print(f"  ⚠️ Error extracting description: {e}")
        
        # Fotoğraf sayısını bul
        try:
            photo_selectors = [
                "[class*='photo']",
                "[class*='image']",
                ".classified-photos",
                "[data-photo-count]"
            ]
            for selector in photo_selectors:
                try:
                    photos = driver.find_elements(By.CSS_SELECTOR, f"{selector} img, {selector} [class*='photo']")
                    if photos:
                        detail_info["photo_count"] = len(photos)
                        break
                except:
                    continue
        except Exception as e:
            pass
        
        # İlan tarihini bul
        try:
            date_selectors = [
                "[class*='date']",
                "[class*='time']",
                ".classified-date"
            ]
            for selector in date_selectors:
                try:
                    date_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    date_text = date_elem.text.strip()
                    if date_text:
                        detail_info["listing_date"] = date_text
                        break
                except:
                    continue
        except Exception as e:
            pass
        
    except Exception as e:
        print(f"  ⚠️ Error scraping detail page {detail_url}: {e}")
    
    return detail_info

def scrape_sahibinden_list_with_details(driver, max_details=10):
    """
    Sahibinden.com sayfasındaki ilan listesini çeker ve detay sayfalarına gidip ek bilgileri ekler.
    max_details: Kaç ilanın detay sayfasına gidileceği (performans için sınırlı)
    Returns: List of dictionaries containing listing information with details
    """
    # Önce liste sayfasından temel bilgileri çek
    listings = scrape_sahibinden_list(driver)
    
    if not listings:
        return listings
    
    print(f"\n🔍 Fetching details for {min(max_details, len(listings))} listings...")
    
    # Her ilan için detay sayfasına git (sınırlı sayıda)
    for i, listing in enumerate(listings[:max_details]):
        if listing.get("url") and listing["url"] != "N/A":
            print(f"  📄 [{i+1}/{min(max_details, len(listings))}] Fetching details: {listing.get('title', 'N/A')[:50]}...")
            detail_info = scrape_sahibinden_detail(driver, listing["url"])
            
            # Detay bilgilerini ana listing'e ekle
            listing.update(detail_info)
            
            # Kısa bir bekleme (rate limiting)
            time.sleep(random.uniform(1, 2))
    
    return listings
