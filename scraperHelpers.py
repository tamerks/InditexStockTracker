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

# Function to check stock availability (For ZARA)
def check_stock_zara(driver, sizes_to_check):
    try:
        wait = WebDriverWait(driver, 60)

        # Close the cookie alert if it appears
        try:
            print("Checking for cookie alert...")
            accept_cookies_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
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
        wait = WebDriverWait(driver, 10)

        # Handle cookie popup if present
        try:
            print("Checking for cookie alert...")
            accept_cookies_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
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
        wait = WebDriverWait(driver, 60)
        
        # Close the cookie alert if it appears
        try:
            print("Checking for cookie alert...")
            accept_cookies_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
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
