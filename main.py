from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time

# Path to your ChromeDriver
chrome_driver_path = "Your Chrome Driver Path"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the Cookie Clicker game
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Wait for the game to load
time.sleep(5)

# Get the cookie to click on
cookie = driver.find_element(By.ID, "bigCookie")


# Function to get upgrade item ids
def get_item_ids():
    items = driver.find_elements(By.CSS_SELECTOR, "#store div")
    return [item.get_attribute("id") for item in items if item.get_attribute("id")]


# Get initial upgrade item ids
item_ids = get_item_ids()

# Initialize timeout
timeout = time.time() + 5

while True:
    try:
        # Click the cookie
        cookie.click()

        # Every 5 seconds:
        if time.time() > timeout:
            # Get all upgrade <b> tags
            all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
            item_prices = []

            # Convert <b> text into an integer price
            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    try:
                        cost = int(element_text.split("-")[1].strip().replace(",", ""))
                        item_prices.append(cost)
                    except (IndexError, ValueError):
                        # Ignore elements that do not have a valid price
                        continue

            # Create dictionary of store items and prices
            cookie_upgrades = {}
            for n in range(len(item_prices)):
                cookie_upgrades[item_prices[n]] = item_ids[n]

            # Get current cookie count
            money_element = driver.find_element(By.ID, "cookies").text.split(" ")[0]
            if "," in money_element:
                money_element = money_element.replace(",", "")
            cookie_count = int(money_element)

            # Find upgrades that we can currently afford
            affordable_upgrades = {}
            for cost, id in cookie_upgrades.items():
                if cookie_count >= cost:
                    affordable_upgrades[cost] = id

            # Purchase the most expensive affordable upgrade
            if affordable_upgrades:
                highest_price_affordable_upgrade = max(affordable_upgrades)
                print(f"Purchasing upgrade: {highest_price_affordable_upgrade}")
                to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

                driver.find_element(By.ID, to_purchase_id).click()

            # Add another 5 seconds until the next check
            timeout = time.time() + 5

    except StaleElementReferenceException:
        # Re-fetch the elements
        cookie = driver.find_element(By.ID, "bigCookie")
        item_ids = get_item_ids()
