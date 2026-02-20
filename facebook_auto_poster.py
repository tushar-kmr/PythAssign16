# facebook_auto_poster.py
# This script automates posting a status on Facebook using Selenium
# I'm using Firefox with geckodriver for this assignment

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import time

# --- My credentials (I know this isnt the safest way but it works for now) ---
# TODO: maybe move these to a .env file later if I have time
# its fake account - BTW :)
fb_email = "csrog.gaming@gmail.com"
fb_password = "Ayush@2646"
my_post_text = "Hello everyone! This is an automated post from my Python assignment 🐍"

# path to geckodriver - make sure this is correct for your machine
# I kept getting "geckodriver not found" errors until I put the full path
gecko_path = "./geckodriver.exe"

# --- Setting up the browser ---
print("Starting the script...")
print("Setting up Firefox browser...")

service = Service(executable_path=gecko_path)
driver = webdriver.Firefox(service=service)

# making the browser full screen so all elements are visible
# (had issues with elements not being clickable when window was small)
driver.maximize_window()

# my wait object - using 5 seconds because facebook can be slow sometimes
my_wait = WebDriverWait(driver, 5)

try:
    # ============ STEP 1: Go to Facebook ============
    print("Navigating to Facebook...")
    driver.get("https://www.facebook.com/")
    time.sleep(3)  # Had to add a sleep here because the page wasn't loading fast enough and threw an error
    print("Debug: Page loaded successfully")

    # ============ STEP 2: Handle the cookie popup if it shows up ============
    # Facebook sometimes shows a cookie consent dialog, need to handle it
    try:
        print("Debug: Looking for cookie popup...")
        # cookie_btn = driver.find_element(By.CLASS_NAME, "cookie-btn")  <-- didn't work, class name was different
        cookie_button = my_wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-cookiebanner="accept_button"]'))
        )
        cookie_button.click()
        print("Debug: Clicked the cookie accept button")
        time.sleep(1)
    except:
        # sometimes the cookie popup doesn't show up, thats fine
        print("No cookie popup found, moving on...")

    # ============ STEP 3: Login to Facebook ============
    print("Debug: Looking for login fields...")

    # finding the email input field using ID
    email_field = my_wait.until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    print("Debug: Successfully found the email input field")
    email_field.clear()
    email_field.send_keys(fb_email)
    print("Debug: Entered email address")

    # finding password field using ID
    pass_field = driver.find_element(By.NAME, "pass")
    pass_field.clear()
    pass_field.send_keys(fb_password)
    print("Debug: Entered password")

    # clicking the login button using name attribute
    # facebook always changes layout of button so finally this worked for me
    the_button = my_wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[text()='Log in']]"))
    )
    the_button.click()
    print("Debug: Clicked login button")

    # waiting for the page to load after login
    print("waiting for 5 seconds... letting the page load")
    time.sleep(5)

    # quick check - see if we actually logged in by looking at the URL
    current = driver.current_url
    print(f"Debug: Current URL after login = {current}")

    # ============ STEP 4: Find the "What's on your mind?" box and click it ============
    print("Debug: Looking for the post input area...")

    # the post box on facebook is tricky - its not a regular input field
    # I had to use xpath to find it because there's no good ID for it
    # elem = driver.find_element(By.CLASS_NAME, "mentionsTextarea")  <-- didn't work, old facebook layout maybe?
    post_box = my_wait.until(
        EC.element_to_be_clickable(By.XPATH, '//span[contains(text(), "What\'s on your mind")]')
    )
    post_box.click()
    print("Debug: Clicked on the 'Whats on your mind' area")

    # need to wait a bit for the post dialog to fully open
    time.sleep(3)
    print("waiting for 5 seconds... post dialog should be opening")

    # ============ STEP 5: Type the post content ============
    print("Debug: Looking for the text area inside the dialog...")

    # now I need to find the actual text area inside the popup dialog
    # this was the hardest part - the text area is inside a editable div
    text_area = my_wait.until(
        EC.element_to_be_clickable(By.XPATH, "//div[@contenteditable='true' and @role='textbox']")
    )
    text_area.click()
    time.sleep(1)

    # typing out the post text
    text_area.send_keys(my_post_text)
    print(f"Debug: Typed the post text: '{my_post_text}'")

    # small pause to make sure text is fully entered
    time.sleep(2)

    # ============ STEP 6: Click the Post button ============
    print("Debug: Looking for the Post button...")

    # finding the post/submit button
    post_button = my_wait.until(
        EC.element_to_be_clickable(By.XPATH, "//div[@role='button' and @aria-label='Post']")
    )
    post_button.click()
    print("Debug: Clicked the Post button!")

    # wait for the post to actually go through
    time.sleep(5)
    print("waiting for 5 seconds... post should be publishing")

    print("\n========================================")
    print("SUCCESS! Post has been published!")
    print("========================================\n")

except Exception as e:
    # if anything goes wrong, just print the error so I can see what happened
    print(f"\nSomething went wrong :( Here's the error: {e}")

finally:
    # always close the browser when done, even if there was an error
    print("Closing the browser...")
    time.sleep(2)
    driver.quit()
    print("Browser closed. Script finished.")
