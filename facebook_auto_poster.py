import time

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- Credentials ---
FACEBOOK_EMAIL = "email@gmail.com"
FACEBOOK_PASSWORD = "Password123"
POST_MESSAGE = "Hello from my automated poster!"

# --- GeckoDriver path (same folder as this script) ---
GECKODRIVER_PATH = str(Path(__file__).resolve().parent / "geckodriver.exe")
TIMEOUT = 20


def type_slowly(element, text):
    for ch in text:
        element.send_keys(ch)
        time.sleep(0.12)


# --- Set up Firefox browser ---
options = Options()
options.set_preference("dom.webnotifications.enabled", False)
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

service = Service(executable_path=GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)
driver.maximize_window()

try:
    # 1. Open Facebook
    print("Opening Facebook...")
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    # 3. Enter email
    print("Logging in...")
    email_field = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    type_slowly(email_field, FACEBOOK_EMAIL)
    time.sleep(3)

    # 4. Enter password
    password_field = driver.find_element(By.NAME, "pass")
    type_slowly(password_field, FACEBOOK_PASSWORD)
    time.sleep(3)

    # 5. Click login
    driver.find_element(By.NAME, "login").click()
    print("Login button clicked, waiting for home page...")

    # 6. Wait for home page to load
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@role='navigation'] | //div[@aria-label='Create a post']")
        )
    )
    print("Logged in successfully!")
    time.sleep(3)

    # 7. Click "What's on your mind?" to open the post composer
    print("Opening post composer...")
    post_prompt = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//span[contains(text(), \"What's on your mind\")]"
             " | //div[@aria-label=\"Create a post\"]")
        )
    )
    post_prompt.click()
    time.sleep(3)

    # 8. Type the message
    post_box = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//div[@role='dialog']//div[@role='textbox']"
             " | //div[@contenteditable='true'][@role='textbox']")
        )
    )
    post_box.click()
    time.sleep(3)
    type_slowly(post_box, POST_MESSAGE)
    print("Message typed.")
    time.sleep(3)

    # 9. Click Post
    post_button = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//div[@aria-label='Post']"
             " | //span[text()='Post']/ancestor::div[@role='button']")
        )
    )
    post_button.click()
    print("Post submitted!")
    time.sleep(3)

except (TimeoutException, NoSuchElementException) as e:
    print(f"Error: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Screenshot saved as error_screenshot.png")

finally:
    driver.quit()
    print("Browser closed.")
